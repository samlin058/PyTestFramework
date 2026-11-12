import allure
import pytest

from domain.business.ui.AITF.login_biz import LoginBiz
from service.assert_utils import AssertUtils
from service.data_driver import parametrize_data


@allure.story("登录页面测试")
@pytest.mark.parametrize("case", parametrize_data("login_cases.yaml"))
def test_login_page(page, case):
    biz = LoginBiz(page)
    biz.login(case["username"], case["password"])
    if case.get("expect"):
        AssertUtils.equal(page.url, case["expect"])

