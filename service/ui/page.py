from __future__ import annotations

from playwright.sync_api import Locator, Page

from service.ui.elements_loader import load_ui_elements


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

    def url(self) -> str:
        """当前浏览器地址栏 URL。"""
        return self.page.url

    def title(self) -> str:
        """当前页面 title。"""
        return self.page.title()

    def wait_url(self, url_or_pattern: str, *, timeout_ms: int | None = None) -> None:
        """等待地址栏匹配指定 URL 或正则（如 ``**/dashboard**``）。"""
        self.page.wait_for_url(
            url_or_pattern,
            timeout=self.timeout_ms if timeout_ms is None else timeout_ms,
        )

    def reload(self) -> None:
        self.page.reload(wait_until="domcontentloaded", timeout=self.timeout_ms)

    def locator(self, name: str) -> Locator:
        return self.page.locator(self.el(name))

    def click(self, name: str) -> None:
        self.locator(name).click(timeout=self.timeout_ms)

    def type(self, name: str, text: str | int | float, clear: bool = True) -> None:
        # YAML 未加引号时数字会变成 int/float；Playwright fill/type 只接受 str
        value = text if isinstance(text, str) else str(text)
        loc = self.locator(name)
        if clear:
            loc.fill(value, timeout=self.timeout_ms)
        else:
            loc.type(value, timeout=self.timeout_ms)

    def text_of(self, name: str) -> str:
        return self.locator(name).inner_text(timeout=self.timeout_ms)

    def get_attribute(self, name: str, attr: str) -> str | None:
        return self.locator(name).get_attribute(attr, timeout=self.timeout_ms)

    def screenshot_png(self) -> bytes:
        return self.page.screenshot(type="png", full_page=True)
