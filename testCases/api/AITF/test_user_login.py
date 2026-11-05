from __future__ import annotations

import allure
import pytest

from business.api.AITF.user_biz import UserBiz
from core.assert_utils import AssertUtils
from core.data_driver import parametrize_data


@allure.feature("API")
@allure.story("User Login")
@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.parametrize("case", parametrize_data("api/AITF/login_cases.yaml"))
def test_user_login(http_client, user_factory, case):
    account = user_factory.prepare_login_account()
    biz = UserBiz(http_client)

    if case.get("expect_success"):
        email = case.get("email") or account["email"]
        password = case.get("password") or account["password"]
        resp = biz.login(email, password)
        AssertUtils.status_code(resp, 200)
        AssertUtils.contains(resp.json(), "token")
    else:
        resp = biz.login(case["email"], case.get("password", ""))
        AssertUtils.status_code(resp, case.get("expected_status", 400))


@allure.feature("API")
@allure.story("User Factory")
@pytest.mark.api
def test_create_user_via_factory(user_factory):
    user = user_factory.create_user(name="factory_user", job="qa")
    AssertUtils.true(bool(user.get("id")), "created user should have id")
    AssertUtils.equal(user.get("name"), "factory_user")
