from __future__ import annotations

import allure
from playwright.sync_api import Page

from service.config import get_project_config
from service.ui import UiBizBase


class LoginBiz(UiBizBase):
    """AITF UI 登录业务：封装登录页操作流程。"""
    def __init__(self, page: Page | None = None, *, project: str = "AITF") -> None:
        super().__init__(page, project=project, elements="login")

    @allure.step("业务: UI 登录")
    def login(self, username: str, password: str) -> None:
        base_url = get_project_config("AITF").get("ui").get("base_url")
        self.ui.open(base_url)
        self.ui.type("account", username)
        self.ui.type("password", password)
        self.ui.click("submit")



if __name__ == "__main__":
    # 独立调试：python -m domain.business.ui.AITF.login_biz
    username = get_project_config("AITF").get("global_var").get("user")
    password = get_project_config("AITF").get("global_var").get("password")
    biz = LoginBiz()
    try:
        biz.login(username, password)
        biz.ui.page.wait_for_timeout(3000)
    finally:
        biz.close()
