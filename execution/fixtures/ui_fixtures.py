from __future__ import annotations

from typing import Any

import pytest
from playwright.sync_api import Browser, Page, Playwright, sync_playwright

from core.config import get_config


@pytest.fixture
def ui_base_url(project_config: dict[str, Any]) -> str:
    """读取当前项目配置中的 UI 入口地址。"""
    configured = ((project_config.get("ui") or {}).get("base_url") or "").strip()
    if not configured:
        project = project_config.get("project", "<unknown>")
        raise pytest.UsageError(
            f"UI base_url is not configured for project {project!r}. "
            f"Set projects.{project}.ui.base_url in config/*.yaml or UI_BASE_URL env."
        )
    return configured.rstrip("/")


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Browser:
    """按 defaults.ui.headless 启动 Chromium。"""
    cfg = (get_config().get("defaults") or {}).get("ui") or {}
    browser = playwright_instance.chromium.launch(headless=bool(cfg.get("headless", True)))
    yield browser
    browser.close()


@pytest.fixture
def page(browser: Browser, project_config: dict[str, Any]) -> Page:
    """按当前项目 UI 超时配置创建独立 context + page。"""
    cfg = project_config.get("ui") or {}
    default_timeout_ms = int(cfg.get("default_timeout", 10)) * 1000
    navigation_timeout_ms = int(cfg.get("navigation_timeout", 30)) * 1000

    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()
    page.set_default_timeout(default_timeout_ms)
    page.set_default_navigation_timeout(navigation_timeout_ms)
    yield page
    context.close()
