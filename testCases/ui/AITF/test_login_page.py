import allure
import pytest

from business.ui.AITF.login_biz import LoginBiz
from core.assert_utils import AssertUtils
from core.data_driver import parametrize_data


@allure.story("Login Page")
@pytest.mark.parametrize("case", parametrize_data("login_cases.yaml"))
def test_login_page(page, case):
    biz = LoginBiz(page)
    msg = biz.login(case["username"], case["password"])
    if case.get("expect_success"):
        AssertUtils.contains(msg, "Login success")
    else:
        AssertUtils.contains(msg, "Login failed")
