from __future__ import annotations

import os
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from service.config import resolve_project_name


@dataclass
class RunSummary:
    """Aggregated pytest run statistics for notification payloads."""

    passed: int = 0
    failed: int = 0
    skipped: int = 0
    error: int = 0
    xfailed: int = 0
    xpassed: int = 0
    duration: float = 0.0
    failed_names: list[str] = field(default_factory=list)
    env: str = "test"
    report_url: str = ""
    project: str = ""

    @property
    def total(self) -> int:
        return (
            self.passed
            + self.failed
            + self.skipped
            + self.error
            + self.xfailed
            + self.xpassed
        )

    @property
    def is_success(self) -> bool:
        return self.failed == 0 and self.error == 0


_OUTCOME_KEYS = ("passed", "failed", "skipped", "error", "xfailed", "xpassed")


def _project_from_parts(parts: tuple[str, ...] | list[str]) -> str | None:
    if "testCases" not in parts:
        return None
    idx = parts.index("testCases")
    if len(parts) > idx + 2 and parts[idx + 1] in {"api", "ui"}:
        return parts[idx + 2]
    return None


def _project_from_report(rep: Any) -> str | None:
    """Resolve project name from a TestReport nodeid / fspath."""
    candidates: list[str] = []
    nodeid = getattr(rep, "nodeid", None)
    if nodeid:
        candidates.append(str(nodeid).split("::", 1)[0])
    for attr in ("path", "fspath"):
        value = getattr(rep, attr, None)
        if value is not None:
            candidates.append(str(value))

    for raw in candidates:
        path = Path(raw)
        found = _project_from_parts(path.parts)
        if found:
            return found
        try:
            return resolve_project_name(path)
        except ValueError:
            continue
    return None


def _empty_bucket() -> dict[str, Any]:
    return {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "error": 0,
        "xfailed": 0,
        "xpassed": 0,
        "duration": 0.0,
        "failed_names": [],
    }


def collect_from_terminalreporter(terminalreporter: Any, *, duration: float | None = None) -> RunSummary:
    """Build a session-wide RunSummary from pytest's TerminalReporter."""
    by_project = collect_by_project(terminalreporter, duration=duration)
    if len(by_project) == 1:
        return next(iter(by_project.values()))

    stats = getattr(terminalreporter, "stats", {}) or {}

    def _count(key: str) -> int:
        return len(stats.get(key, []) or [])

    failed_names: list[str] = []
    for key in ("failed", "error"):
        for rep in stats.get(key, []) or []:
            nodeid = getattr(rep, "nodeid", None) or str(rep)
            if nodeid not in failed_names:
                failed_names.append(nodeid)

    session_duration = duration
    if session_duration is None:
        session_duration = _session_duration(terminalreporter)

    return RunSummary(
        passed=_count("passed"),
        failed=_count("failed"),
        skipped=_count("skipped"),
        error=_count("error"),
        xfailed=_count("xfailed"),
        xpassed=_count("xpassed"),
        duration=session_duration,
        failed_names=failed_names,
        env=os.getenv("ENV", "test").strip().lower() or "test",
        report_url=_resolve_report_url(),
    )


def collect_by_project(
    terminalreporter: Any,
    *,
    duration: float | None = None,
) -> dict[str, RunSummary]:
    """Split TerminalReporter stats into per-project RunSummary map."""
    stats = getattr(terminalreporter, "stats", {}) or {}
    buckets: dict[str, dict[str, Any]] = defaultdict(_empty_bucket)
    unknown = "__unknown__"

    for outcome in _OUTCOME_KEYS:
        for rep in stats.get(outcome, []) or []:
            project = _project_from_report(rep) or unknown
            bucket = buckets[project]
            bucket[outcome] += 1
            bucket["duration"] += float(getattr(rep, "duration", 0.0) or 0.0)
            if outcome in {"failed", "error"}:
                nodeid = getattr(rep, "nodeid", None) or str(rep)
                if nodeid not in bucket["failed_names"]:
                    bucket["failed_names"].append(nodeid)

    if not buckets:
        return {}

    env = os.getenv("ENV", "test").strip().lower() or "test"
    report_url = _resolve_report_url()
    session_duration = duration if duration is not None else _session_duration(terminalreporter)

    result: dict[str, RunSummary] = {}
    for project, bucket in buckets.items():
        # Prefer summed test durations; fall back to session duration for single-project runs.
        proj_duration = float(bucket["duration"] or 0.0)
        if proj_duration <= 0 and len(buckets) == 1:
            proj_duration = session_duration
        name = "" if project == unknown else project
        result[project] = RunSummary(
            passed=bucket["passed"],
            failed=bucket["failed"],
            skipped=bucket["skipped"],
            error=bucket["error"],
            xfailed=bucket["xfailed"],
            xpassed=bucket["xpassed"],
            duration=proj_duration,
            failed_names=list(bucket["failed_names"]),
            env=env,
            report_url=report_url,
            project=name,
        )
    return result


def _session_duration(terminalreporter: Any) -> float:
    session_start = getattr(terminalreporter, "_session_start", None)
    if session_start is None:
        return 0.0
    import time

    return max(0.0, time.time() - float(session_start))


def _resolve_report_url() -> str:
    for key in ("NOTIFY_REPORT_URL", "ALLURE_REPORT_URL", "BUILD_URL"):
        value = (os.getenv(key) or "").strip()
        if value:
            if key == "BUILD_URL" and not value.rstrip("/").endswith("allure"):
                return value.rstrip("/") + "/allure"
            return value
    return ""


def format_duration(seconds: float) -> str:
    total = max(0, int(round(seconds)))
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}h{minutes}m{secs}s"
    if minutes:
        return f"{minutes}m{secs}s"
    return f"{secs}s"


def _title_with_project(title: str, project: str) -> str:
    if project and project not in title:
        return f"{title} / {project}"
    return title


def format_text(summary: RunSummary, *, title: str = "PyTestFramework", max_failed: int = 10) -> str:
    """Plain-text body shared by text message types."""
    status = "成功" if summary.is_success else "失败"
    display_title = _title_with_project(title, summary.project)
    lines = [
        f"【{display_title}】{summary.env} 环境执行{status}",
        f"通过: {summary.passed} | 失败: {summary.failed} | 错误: {summary.error} | 跳过: {summary.skipped}",
        f"总计: {summary.total} | 耗时: {format_duration(summary.duration)}",
    ]
    if summary.xfailed or summary.xpassed:
        lines.append(f"xfail: {summary.xfailed} | xpass: {summary.xpassed}")
    if summary.report_url:
        lines.append(f"报告: {summary.report_url}")
    if summary.failed_names:
        lines.append("失败用例:")
        for name in summary.failed_names[: max(0, max_failed)]:
            lines.append(f"- {name}")
        extra = len(summary.failed_names) - max(0, max_failed)
        if extra > 0:
            lines.append(f"... 另有 {extra} 条")
    return "\n".join(lines)


def format_markdown(summary: RunSummary, *, title: str = "PyTestFramework", max_failed: int = 10) -> str:
    """Markdown body compatible with WeCom / DingTalk robots."""
    status = "成功" if summary.is_success else "失败"
    display_title = _title_with_project(title, summary.project)
    lines = [
        f"## 【{display_title}】{summary.env} 环境执行{status}",
        f"- 通过: **{summary.passed}**",
        f"- 失败: **{summary.failed}**",
        f"- 错误: **{summary.error}**",
        f"- 跳过: **{summary.skipped}**",
        f"- 总计: **{summary.total}** | 耗时: **{format_duration(summary.duration)}**",
    ]
    if summary.xfailed or summary.xpassed:
        lines.append(f"- xfail: {summary.xfailed} | xpass: {summary.xpassed}")
    if summary.report_url:
        lines.append(f"- 报告: [打开 Allure]({summary.report_url})")
    if summary.failed_names:
        lines.append("")
        lines.append("**失败用例**")
        for name in summary.failed_names[: max(0, max_failed)]:
            lines.append(f"- `{name}`")
        extra = len(summary.failed_names) - max(0, max_failed)
        if extra > 0:
            lines.append(f"- ... 另有 {extra} 条")
    return "\n".join(lines)
