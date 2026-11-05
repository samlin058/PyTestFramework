from __future__ import annotations

import allure
import pytest

from business.ui.login_biz import LoginBiz
from core.assert_utils import AssertUtils
from core.data_driver import parametrize_data


@allure.feature("UI")
@allure.story("Login Page")
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.parametrize("case", parametrize_data("ui/login_cases.yaml"))
def test_login_page(page, ui_base_url, case):
    biz = LoginBiz(page, ui_base_url)
    msg = biz.login(case["username"], case["password"])
    if case.get("expect_success"):
        AssertUtils.contains(msg, "Login success")
    else:
        AssertUtils.contains(msg, "Login failed")
