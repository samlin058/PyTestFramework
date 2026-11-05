from __future__ import annotations

import allure
from playwright.sync_api import Page

from assets.ui.pages.login_page import LoginPage


class LoginBiz:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = LoginPage(page)
        self.base_url = base_url

    @allure.step("业务: UI 登录")
    def login(self, username: str, password: str) -> str:
        self.page.open_login(self.base_url)
        self.page.login(username, password)
        return self.page.message()
