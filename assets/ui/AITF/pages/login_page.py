from __future__ import annotations

from assets.ui.AITF.pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = "#username"
    PASSWORD = "#password"
    SUBMIT = "#login-btn"
    MESSAGE = "#message"

    def open_login(self, base_url: str) -> None:
        self.open(base_url)

    def login(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def message(self) -> str:
        return self.text_of(self.MESSAGE)
