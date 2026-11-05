from __future__ import annotations

import re
from pathlib import Path

import allure
import pytest

_TESTCASES_ROOT = Path(__file__).resolve().parents[2] / "testCases"


def pytest_configure(config):  # noqa: ARG001
    """Hook placeholder; markers are declared in pytest.ini."""


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

    例如 ``pytest -m api`` 不收集 ``testCases/ui``；``pytest -m ui`` 不收集 ``testCases/api``。
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
