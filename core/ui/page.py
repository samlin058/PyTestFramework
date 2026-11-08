from __future__ import annotations

from playwright.sync_api import Locator, Page

from core.ui.elements_loader import load_ui_elements


class UiPage:
    """通用页面元素操作：绑定 Playwright Page + elements YAML。"""

    def __init__(
        self,
        page: Page,
        *,
        project: str,
        elements: str,
        timeout_ms: int = 10000,
    ) -> None:
        self.page = page
        self.project = project
        self.elements_name = elements
        self.timeout_ms = timeout_ms
        self._elements = load_ui_elements(project, elements)

    def el(self, name: str) -> str:
        """按元素名取 selector。"""
        try:
            return self._elements[name]
        except KeyError as exc:
            raise KeyError(
                f"Element {name!r} not found in {self.project}/{self.elements_name}.yaml; "
                f"available: {sorted(self._elements)}"
            ) from exc

    def open(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def locator(self, name: str) -> Locator:
        return self.page.locator(self.el(name))

    def click(self, name: str) -> None:
        self.locator(name).click(timeout=self.timeout_ms)

    def type(self, name: str, text: str, clear: bool = True) -> None:
        loc = self.locator(name)
        if clear:
            loc.fill(text, timeout=self.timeout_ms)
        else:
            loc.type(text, timeout=self.timeout_ms)

    def text_of(self, name: str) -> str:
        return self.locator(name).inner_text(timeout=self.timeout_ms)

    def screenshot_png(self) -> bytes:
        return self.page.screenshot(type="png", full_page=True)
