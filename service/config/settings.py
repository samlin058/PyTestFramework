from __future__ import annotations

import os
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from service.utils.path_util import PROJECT_ROOT

_CONFIG: dict[str, Any] | None = None


def _env_name() -> str:
    """读取当前运行环境名（ENV），默认 test。"""
    return os.getenv("ENV", "test").strip().lower()


def _load_yaml(env: str) -> dict[str, Any]:
    """加载指定环境的 service/config/<env>.yaml 配置文件。"""
    path = PROJECT_ROOT / "service" / "config" / f"{env}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """深度合并字典，override 覆盖 base 中同名键。"""
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def _env_flag(name: str) -> bool | None:
    """解析布尔环境变量；未设置返回 None。"""
    raw = os.getenv(name)
    if raw is None:
        return None
    return raw.strip().lower() in {"1", "true", "yes"}


def _apply_notify_env(notify: dict[str, Any], *, prefix: str = "NOTIFY") -> None:
    """Apply NOTIFY_* or NOTIFY_<PROJECT>_* overrides onto a notify dict.

    Channel-style keys (preferred)::

        NOTIFY_WECOM_WEBHOOK
        NOTIFY_DINGTALK_WEBHOOK / NOTIFY_DINGTALK_SECRET
        NOTIFY_AITF_WECOM_WEBHOOK / NOTIFY_AITF_DINGTALK_WEBHOOK

    Legacy flat keys (``NOTIFY_WEBHOOK`` + ``NOTIFY_PROVIDER``) still work.
    """
    title = os.getenv(f"{prefix}_TITLE")
    report_url = os.getenv(f"{prefix}_REPORT_URL")
    if prefix == "NOTIFY" and not report_url:
        report_url = os.getenv("ALLURE_REPORT_URL")
    enabled = _env_flag(f"{prefix}_ENABLED")
    mention_all = _env_flag(f"{prefix}_MENTION_ALL_ON_FAIL")

    if title:
        notify["title"] = title
    if report_url:
        notify["report_url"] = report_url
    if enabled is not None:
        notify["enabled"] = enabled
    if mention_all is not None:
        notify["mention_all_on_fail"] = mention_all

    wecom = notify.setdefault("wecom", {})
    dingtalk = notify.setdefault("dingtalk", {})
    wecom_webhook = os.getenv(f"{prefix}_WECOM_WEBHOOK")
    dingtalk_webhook = os.getenv(f"{prefix}_DINGTALK_WEBHOOK")
    dingtalk_secret = os.getenv(f"{prefix}_DINGTALK_SECRET")
    if wecom_webhook:
        wecom["webhook"] = wecom_webhook
    if dingtalk_webhook:
        dingtalk["webhook"] = dingtalk_webhook
    if dingtalk_secret:
        dingtalk["secret"] = dingtalk_secret

    # Legacy flat webhook/provider/secret → map into one channel
    webhook = os.getenv(f"{prefix}_WEBHOOK")
    provider = (os.getenv(f"{prefix}_PROVIDER") or "").strip().lower()
    secret = os.getenv(f"{prefix}_SECRET")
    if webhook:
        notify["webhook"] = webhook
        if provider in {"dingtalk", "dingding", "ding"} or "oapi.dingtalk.com" in webhook.lower():
            dingtalk.setdefault("webhook", webhook)
            if secret:
                dingtalk.setdefault("secret", secret)
        else:
            wecom.setdefault("webhook", webhook)
    if provider:
        notify["provider"] = provider
    if secret:
        notify["secret"] = secret
        if provider in {"dingtalk", "dingding", "ding"}:
            dingtalk.setdefault("secret", secret)


def _apply_project_env_overrides(project_cfg: dict[str, Any]) -> None:
    """将命令行/系统环境变量覆盖到单个项目配置（api/db/ui）。"""
    if os.getenv("API_BASE_URL"):
        project_cfg["api_base_url"] = os.getenv("API_BASE_URL")
    db = project_cfg.setdefault("db", {})
    for key, env_key in (
        ("host", "DB_HOST"),
        ("port", "DB_PORT"),
        ("user", "DB_USER"),
        ("password", "DB_PASSWORD"),
        ("database", "DB_NAME"),
    ):
        if os.getenv(env_key):
            value = os.getenv(env_key)
            db[key] = int(value) if key == "port" else value
    ui = project_cfg.setdefault("ui", {})
    if os.getenv("UI_BASE_URL"):
        ui["base_url"] = os.getenv("UI_BASE_URL")


def _apply_env_overrides(cfg: dict[str, Any]) -> dict[str, Any]:
    """用环境变量覆盖 notify、defaults.ui.headless，以及指定/全部项目的 api_base_url、db、ui。"""
    notify = cfg.setdefault("notify", {})
    _apply_notify_env(notify, prefix="NOTIFY")

    defaults_ui = cfg.setdefault("defaults", {}).setdefault("ui", {})
    headless = _env_flag("UI_HEADLESS")
    if headless is not None:
        defaults_ui["headless"] = headless

    projects = cfg.setdefault("projects", {})
    target = (os.getenv("PROJECT") or "").strip()
    names = [target] if target and target in projects else list(projects.keys())
    for name in names:
        project_cfg = projects.setdefault(name, {})
        _apply_project_env_overrides(project_cfg)
        if target and target == name:
            # PROJECT=AITF 时，全局 NOTIFY_* 同时落到该项目（可被 NOTIFY_AITF_* 再覆盖）
            _apply_notify_env(project_cfg.setdefault("notify", {}), prefix="NOTIFY")

    # 任意项目均可使用 NOTIFY_<PROJECT>_WEBHOOK 等覆盖
    for name, project_cfg in projects.items():
        _apply_notify_env(project_cfg.setdefault("notify", {}), prefix=f"NOTIFY_{name}")
    return cfg


@lru_cache(maxsize=1)
def get_config() -> dict[str, Any]:
    """获取当前环境的完整配置（含 projects），首次调用时加载并应用环境变量覆盖。"""
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = _apply_env_overrides(_load_yaml(_env_name()))
    return _CONFIG


def list_projects() -> list[str]:
    """返回当前环境配置中的项目名列表。"""
    return list((get_config().get("projects") or {}).keys())


def get_project_config(project: str) -> dict[str, Any]:
    """按项目名加载配置：defaults 与 projects.<name> 深度合并。

    ``notify`` 单独处理：全局 ``notify`` 为底，项目 ``projects.<name>.notify`` 覆盖。
    """
    cfg = get_config()
    projects = cfg.get("projects") or {}
    if project not in projects:
        available = ", ".join(projects) or "(none)"
        raise KeyError(f"Project {project!r} not found in config. Available: {available}")
    raw_project = projects[project] or {}
    project_body = {k: v for k, v in raw_project.items() if k != "notify"}
    merged = _deep_merge(cfg.get("defaults") or {}, project_body)
    merged["project"] = project
    merged["env"] = cfg.get("env")
    merged["notify"] = _deep_merge(deepcopy(cfg.get("notify") or {}), deepcopy(raw_project.get("notify") or {}))
    return merged


def resolve_project_name(path: str | Path) -> str:
    """从用例路径解析项目名，约定 application/testCases/<api|ui>/<project>/..."""
    parts = Path(path).resolve().parts
    try:
        idx = parts.index("testCases")
    except ValueError as exc:
        raise ValueError(f"Path is not under application/testCases: {path}") from exc
    if len(parts) <= idx + 2:
        raise ValueError(
            f"Cannot resolve project from path {path}; "
            f"expected application/testCases/<api|ui>/<project>/..."
        )
    layer = parts[idx + 1]
    if layer not in {"api", "ui"}:
        raise ValueError(f"Unexpected test layer {layer!r} in path {path}")
    return parts[idx + 2]


def reload_config() -> dict[str, Any]:
    """清除配置缓存并重新加载，返回最新配置。"""
    global _CONFIG
    get_config.cache_clear()
    _CONFIG = None
    return get_config()
