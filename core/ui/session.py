from __future__ import annotations

from types import TracebackType
from typing import Any

from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from core.config import get_project_config


class UiSession:
    """与 pytest 无关的 UI 会话：按项目合并配置自启 Chromium（固定有头）。"""

    def __init__(self, project: str) -> None:
        self.project = project
        self.base_url: str = ""
        self.page: Page | None = None
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None

    def __enter__(self) -> UiSession:
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def start(self) -> Page:
        """启动 Playwright / Chromium / context / page，返回 page。"""
        if self.page is not None:
            return self.page

        cfg = get_project_config(self.project)
        ui: dict[str, Any] = cfg.get("ui") or {}
        self.base_url = (ui.get("base_url") or "").strip().rstrip("/")
        default_timeout_ms = int(ui.get("default_timeout", 10)) * 1000
        navigation_timeout_ms = int(ui.get("navigation_timeout", 30)) * 1000

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=False,
            args=["--start-maximized"],
        )
        # no_viewport=True：跟随实际窗口尺寸，配合 --start-maximized 实现自适应全屏
        self._context = self._browser.new_context(no_viewport=True)
        page = self._context.new_page()
        page.set_default_timeout(default_timeout_ms)
        page.set_default_navigation_timeout(navigation_timeout_ms)
        self.page = page
        return page

    def close(self) -> None:
        """关闭 page / context / browser / playwright（幂等）。"""
        if self._context is not None:
            self._context.close()
            self._context = None
        self.page = None
        if self._browser is not None:
            self._browser.close()
            self._browser = None
        if self._playwright is not None:
            self._playwright.stop()
            self._playwright = None
