from __future__ import annotations

from time import sleep

import allure
from playwright.sync_api import Page

from core.config import get_project_config
from core.ui import UiBizBase


class LoginBiz(UiBizBase):
    """AITF UI 登录业务：封装登录页操作流程。"""

    def __init__(self, page: Page | None = None, *, project: str = "AITF") -> None:
        super().__init__(page, project=project, elements="login")

    @allure.step("业务: UI 登录")
    def login(self, username: str, password: str) -> str:
        self.ui.open(self.base_url)
        self.ui.type("account", username)
        self.ui.type("password", password)
        self.ui.click("submit")
        sleep(10)


if __name__ == "__main__":
    # 独立调试：python -m business.ui.AITF.login_biz
    # 账号取自 config/{ENV}.yaml → projects.AITF.global_var
    cfg = get_project_config("AITF")
    gv = cfg.get("global_var") or {}
    username = str(gv.get("user"))
    password = str(gv.get("password"))
    biz = LoginBiz(project="AITF")
    try:
        biz.login(username, password)
        input("按回车关闭浏览器...")
    finally:
        biz.close()
