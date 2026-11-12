from __future__ import annotations

import json
from copy import deepcopy
from typing import Any, Iterator
from urllib import error, request

from service.config import get_config, get_project_config
from service.logger import logger
from service.report_ci.notify import dingtalk, wecom
from service.report_ci.notify.summary import RunSummary, format_markdown, format_text

_CHANNEL_KEYS = ("wecom", "dingtalk")


def _global_notify_cfg() -> dict[str, Any]:
    return normalize_notify_cfg(get_config().get("notify") or {})


def resolve_notify_cfg(project: str | None = None) -> dict[str, Any]:
    """Resolve notify config: global as base, ``projects.<name>.notify`` overrides."""
    if not project or project == "__unknown__":
        return _global_notify_cfg()
    try:
        return normalize_notify_cfg(get_project_config(project).get("notify") or {})
    except KeyError:
        return _global_notify_cfg()


def normalize_notify_cfg(raw: dict[str, Any] | None) -> dict[str, Any]:
    """Normalize notify config into multi-channel shape.

    Preferred::

        notify:
          wecom: {webhook: ...}
          dingtalk: {webhook: ..., secret: ...}

    Legacy flat ``provider`` / ``webhook`` / ``secret`` is still accepted and mapped
    into the corresponding channel.
    """
    cfg = deepcopy(raw or {})
    wecom_cfg = dict(cfg.get("wecom") or {})
    dingtalk_cfg = dict(cfg.get("dingtalk") or {})

    legacy_webhook = str(cfg.get("webhook") or "").strip()
    legacy_secret = str(cfg.get("secret") or "").strip()
    if legacy_webhook:
        provider = _detect_provider(legacy_webhook, cfg.get("provider"))
        if provider == "dingtalk":
            dingtalk_cfg.setdefault("webhook", legacy_webhook)
            if legacy_secret:
                dingtalk_cfg.setdefault("secret", legacy_secret)
        else:
            wecom_cfg.setdefault("webhook", legacy_webhook)

    cfg["wecom"] = wecom_cfg
    cfg["dingtalk"] = dingtalk_cfg
    return cfg


def iter_channels(cfg: dict[str, Any]) -> Iterator[tuple[str, dict[str, Any]]]:
    """Yield enabled channels that have a webhook configured."""
    normalized = normalize_notify_cfg(cfg)
    for name in _CHANNEL_KEYS:
        channel = dict(normalized.get(name) or {})
        if channel.get("enabled") is False:
            continue
        if str(channel.get("webhook") or "").strip():
            yield name, channel


def _detect_provider(webhook: str, configured: str | None) -> str:
    provider = (configured or "").strip().lower()
    if provider in {"wecom", "wechat", "qywx", "workweixin"}:
        return "wecom"
    if provider in {"dingtalk", "dingding", "ding"}:
        return "dingtalk"
    url = (webhook or "").lower()
    if "qyapi.weixin.qq.com" in url:
        return "wecom"
    if "oapi.dingtalk.com" in url:
        return "dingtalk"
    return provider or "wecom"


def post_json(url: str, payload: dict[str, Any], *, timeout: float = 10.0) -> bool:
    """POST JSON payload to a webhook URL."""
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            ok = 200 <= resp.status < 300
            if not ok:
                logger.error(f"Notify webhook HTTP {resp.status}: {body}")
                return False
            try:
                parsed = json.loads(body) if body else {}
            except json.JSONDecodeError:
                parsed = {}
            errcode = parsed.get("errcode", parsed.get("code"))
            if errcode not in (None, 0, "0"):
                logger.error(f"Notify webhook rejected: {body}")
                return False
            logger.info(f"Notify webhook status={resp.status}")
            return True
    except error.URLError as exc:
        logger.error(f"Notify webhook failed: {exc}")
        return False
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Notify webhook failed: {exc}")
        return False


def _send_channel(
    channel: str,
    channel_cfg: dict[str, Any],
    *,
    title: str,
    summary: RunSummary | None = None,
    text_body: str | None = None,
    msgtype: str = "markdown",
    mention_all: bool = False,
    max_failed: int = 10,
) -> bool:
    url = str(channel_cfg.get("webhook") or "").strip()
    if not url:
        return False

    if text_body is not None:
        content = text_body
        use_text = True
    else:
        assert summary is not None
        use_text = msgtype == "text"
        content = (
            format_text(summary, title=title, max_failed=max_failed)
            if use_text
            else format_markdown(summary, title=title, max_failed=max_failed)
        )

    if channel == "dingtalk":
        url = dingtalk.sign_webhook(url, str(channel_cfg.get("secret") or ""))
        if use_text:
            payload = dingtalk.build_text_payload(content, mention_all=mention_all)
        else:
            ding_title = title
            if summary and summary.project and summary.project not in title:
                ding_title = f"{title} / {summary.project}"
            payload = dingtalk.build_markdown_payload(
                ding_title,
                content,
                mention_all=mention_all,
            )
        return post_json(url, payload)

    # wecom
    if use_text:
        payload = wecom.build_mention_text_payload(content, mention_all=mention_all)
        return post_json(url, payload)

    payload = wecom.build_markdown_payload(content)
    ok = post_json(url, payload)
    if mention_all:
        post_json(url, wecom.build_mention_text_payload("请关注失败用例", mention_all=True))
    return ok


def send_webhook(
    title: str,
    content: str,
    webhook: str | None = None,
    *,
    project: str | None = None,
) -> bool:
    """Send a simple text notification to all configured channels."""
    cfg = resolve_notify_cfg(project)
    body = f"{title}\n{content}" if title else content

    if webhook:
        provider = _detect_provider(webhook, cfg.get("provider"))
        channel_cfg = {"webhook": webhook, "secret": cfg.get("secret") or ""}
        if provider == "dingtalk":
            channel_cfg["secret"] = cfg.get("dingtalk", {}).get("secret") or cfg.get("secret") or ""
        return _send_channel(
            provider,
            channel_cfg,
            title=title or "PyTestFramework",
            text_body=body,
            msgtype="text",
        )

    channels = list(iter_channels(cfg))
    if not channels:
        logger.warning(
            f"Notify webhook is empty{f' for project {project}' if project else ''}; skip notification"
        )
        return False

    results = [
        _send_channel(name, ch, title=title or "PyTestFramework", text_body=body, msgtype="text")
        for name, ch in channels
    ]
    return any(results)


def notify_run(
    summary: RunSummary,
    *,
    title: str | None = None,
    webhook: str | None = None,
    project: str | None = None,
) -> bool:
    """Send a run summary to all enabled channels (WeCom and/or DingTalk)."""
    project = project or summary.project or None
    if project and not summary.project:
        summary.project = project

    cfg = resolve_notify_cfg(project)
    if cfg.get("enabled") is False:
        logger.info(
            f"Notify disabled by config{f' for project {project}' if project else ''}; skip notification"
        )
        return False

    if not summary.report_url:
        summary.report_url = str(cfg.get("report_url") or "").strip()

    title = title or str(cfg.get("title") or "PyTestFramework")
    max_failed = int(cfg.get("max_failed_list") or 10)
    mention_all = bool(cfg.get("mention_all_on_fail")) and not summary.is_success
    msgtype = str(cfg.get("msgtype") or "markdown").strip().lower()

    if webhook:
        provider = _detect_provider(webhook, cfg.get("provider"))
        channel_cfg = {
            "webhook": webhook,
            "secret": (cfg.get("dingtalk") or {}).get("secret") or cfg.get("secret") or "",
        }
        logger.info(f"Sending notify for project={project or '(global)'} channel={provider}")
        return _send_channel(
            provider,
            channel_cfg,
            title=title,
            summary=summary,
            msgtype=msgtype,
            mention_all=mention_all,
            max_failed=max_failed,
        )

    channels = list(iter_channels(cfg))
    if not channels:
        logger.warning(
            f"Notify channels empty{f' for project {project}' if project else ''}; skip notification"
        )
        return False

    results: list[bool] = []
    for name, channel_cfg in channels:
        logger.info(f"Sending notify for project={project or '(global)'} channel={name}")
        results.append(
            _send_channel(
                name,
                channel_cfg,
                title=title,
                summary=summary,
                msgtype=msgtype,
                mention_all=mention_all,
                max_failed=max_failed,
            )
        )
    return any(results)


def notify_projects(summaries: dict[str, RunSummary]) -> dict[str, bool]:
    """Send notifications per project summary (each may fan-out to multiple channels)."""
    results: dict[str, bool] = {}
    for key, summary in summaries.items():
        project = summary.project or (None if key == "__unknown__" else key)
        results[key] = notify_run(summary, project=project)
    return results


def notify_from_env(title: str = "PyTestFramework", content: str = "Pipeline finished") -> bool:
    """Lightweight helper for Jenkins / scripts without a pytest session."""
    return send_webhook(title, content)
