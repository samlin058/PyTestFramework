from __future__ import annotations

import pytest
from playwright.sync_api import Browser, Page, Playwright, sync_playwright

from core.config import get_config


@pytest.fixture(scope="session")
def ui_base_url() -> str:
    configured = ((get_config().get("ui") or {}).get("base_url") or "").strip()
    if not configured:
        raise pytest.UsageError(
            "UI base_url is not configured. Set ui.base_url in config/*.yaml or UI_BASE_URL env."
        )
    return configured.rstrip("/")


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Browser:
    cfg = get_config().get("ui") or {}
    browser = playwright_instance.chromium.launch(headless=bool(cfg.get("headless", True)))
    yield browser
    browser.close()


@pytest.fixture
def page(browser: Browser) -> Page:
    cfg = get_config().get("ui") or {}
    default_timeout_ms = int(cfg.get("default_timeout", 10)) * 1000
    navigation_timeout_ms = int(cfg.get("navigation_timeout", 30)) * 1000

    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()
    page.set_default_timeout(default_timeout_ms)
    page.set_default_navigation_timeout(navigation_timeout_ms)
    yield page
    context.close()
