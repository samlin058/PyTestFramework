from __future__ import annotations

import re
import time
from pathlib import Path

import allure
import pytest

from service.utils.path_util import PROJECT_ROOT, ensure_dir

_TESTCASES_ROOT = PROJECT_ROOT / "application" / "testCases"


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):  # noqa: ARG001
    """Pin Allure output to project-root ``reports/`` regardless of cwd."""
    config._pytestframework_session_start = time.time()  # type: ignore[attr-defined]
    results_dir = ensure_dir(PROJECT_ROOT / "reports" / "allure-results")
    # allure-pytest reads ``allure_report_dir`` from ``--alluredir``
    if hasattr(config.option, "allure_report_dir"):
        config.option.allure_report_dir = str(results_dir)


def _positive_mentions(markexpr: str, marker: str) -> bool:
    """标记是否以正向条件出现（排除 ``not marker``）。"""
    cleaned = re.sub(rf"\bnot\s+{re.escape(marker)}\b", " ", markexpr)
    return bool(re.search(rf"\b{re.escape(marker)}\b", cleaned))


def _under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def pytest_ignore_collect(collection_path: Path, config: pytest.Config) -> bool | None:
    """按 -m 在收集阶段跳过无关目录，避免 deselected 进入会话/报表统计。

    例如 ``pytest -m api`` 不收集 ``application/testCases/ui``；
    ``pytest -m ui`` 不收集 ``application/testCases/api``。
    """
    markexpr = (config.getoption("markexpr") or "").strip().lower()
    if not markexpr:
        return None

    path = Path(collection_path)
    api_root = _TESTCASES_ROOT / "api"
    ui_root = _TESTCASES_ROOT / "ui"

    if _under(path, ui_root):
        if re.search(r"\bnot\s+ui\b", markexpr):
            return True
        if _positive_mentions(markexpr, "api") and not _positive_mentions(markexpr, "ui"):
            return True
        return None

    if _under(path, api_root):
        if re.search(r"\bnot\s+api\b", markexpr):
            return True
        if _positive_mentions(markexpr, "ui") and not _positive_mentions(markexpr, "api"):
            return True
        return None

    return None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):  # noqa: ARG001
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
    if report.when == "call" and report.failed:
        # UI 失败截图仅用于 UI 用例；API / 自定义 Item 无 page fixture，直接跳过
        if item.get_closest_marker("api") is not None:
            return
        funcargs = getattr(item, "funcargs", None) or {}
        page = funcargs.get("page")
        if page is not None:
            try:
                png = page.screenshot(type="png", full_page=True)
                allure.attach(png, name="failure_screenshot", attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass


def pytest_terminal_summary(terminalreporter, exitstatus, config):  # noqa: ARG001
    """Push WeCom / DingTalk notification after the whole session finishes.

    Results are split by project (``application/testCases/<api|ui>/<project>/...``)
    and each project is sent to its own ``projects.<name>.notify`` webhook
    (falls back to global ``notify``).
    """
    # xdist workers should not notify; only the controller has full stats.
    workerinput = getattr(config, "workerinput", None)
    if workerinput is not None:
        return

    try:
        import os

        from service.report_ci.notify import RunSummary, collect_by_project, notify_projects, notify_run
    except Exception:
        return

    started = getattr(config, "_pytestframework_session_start", None)
    duration = (time.time() - float(started)) if started is not None else None
    by_project = collect_by_project(terminalreporter, duration=duration)
    if not by_project:
        if exitstatus == 0:
            return
        notify_run(RunSummary(env=(os.getenv("ENV", "test") or "test").strip().lower()))
        return

    # Skip empty successful collection-only sessions.
    total = sum(s.total for s in by_project.values())
    failed = sum(s.failed + s.error for s in by_project.values())
    if total == 0 and failed == 0 and exitstatus == 0:
        return
    notify_projects(by_project)
