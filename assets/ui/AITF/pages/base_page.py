from __future__ import annotations

from playwright.sync_api import Locator, Page


class BasePage:
    def __init__(self, page: Page, timeout_ms: int = 10000) -> None:
        self.page = page
        self.timeout_ms = timeout_ms

    def open(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def click(self, selector: str) -> None:
        self.locator(selector).click(timeout=self.timeout_ms)

    def type(self, selector: str, text: str, clear: bool = True) -> None:
        loc = self.locator(selector)
        if clear:
            loc.fill(text, timeout=self.timeout_ms)
        else:
            loc.type(text, timeout=self.timeout_ms)

    def text_of(self, selector: str) -> str:
        return self.locator(selector).inner_text(timeout=self.timeout_ms)

    def screenshot_png(self) -> bytes:
        return self.page.screenshot(type="png", full_page=True)
