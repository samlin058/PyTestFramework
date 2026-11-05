from __future__ import annotations

import allure
import pytest

from business.api.AITF.user_biz import UserBiz
from core.assert_utils import AssertUtils
from core.data_driver import parametrize_data


@allure.story("User Login")
@pytest.mark.skip(reason="临时跳过")
@pytest.mark.parametrize("case", parametrize_data("login_cases.yaml"))
def test_user_login(http_client, user_factory, case):
    """单接口用例：直接 HttpClient.call，不经 business。"""
    account = user_factory.prepare_login_account()

    if case.get("expect_success"):
        email = case.get("email") or account["email"]
        password = case.get("password") or account["password"]
        resp = http_client.call(
            "UserController",
            "login",
            json={"email": email, "password": password},
        )
        AssertUtils.status_code(resp, 200)
        AssertUtils.contains(resp.json(), "token")
    else:
        resp = http_client.call(
            "UserController",
            "login",
            json={"email": case["email"], "password": case.get("password", "")},
        )
        AssertUtils.status_code(resp, case.get("expected_status", 400))


@allure.story("User Factory")
@pytest.mark.skip(reason="临时跳过")
def test_create_user_via_factory(user_factory):
    user = user_factory.create_user(name="factory_user", job="qa")
    AssertUtils.true(bool(user.get("id")), "created user should have id")
    AssertUtils.equal(user.get("name"), "factory_user")


@allure.story("User Biz Scenario")
@pytest.mark.skip(reason="临时跳过")
def test_login_and_get_user_scene(http_client, user_factory):
    """场景用例：通过 business 串联 login + getUser。"""
    account = user_factory.prepare_login_account()
    biz = UserBiz(http_client)
    result = biz.login_and_get_user(
        email=account["email"],
        password=account["password"],
        user_id=2,
    )

    AssertUtils.status_code(result["login_resp"], 200)
    AssertUtils.true(bool(result.get("token")), "login should return token")
    AssertUtils.status_code(result["get_resp"], 200)
    AssertUtils.contains(result["user"], "data")


@allure.story("User Biz Scenario")
@pytest.mark.skip(reason="临时跳过")
def test_create_user_then_login_scene(http_client, user_factory):
    """场景用例：创建用户后登录，返回 token 上下文。"""
    account = user_factory.prepare_login_account()
    biz = UserBiz(http_client)
    result = biz.create_user_then_login(
        name="login_scene_user",
        job="qa",
        email=account["email"],
        password=account["password"],
    )

    AssertUtils.status_code(result["create_resp"], 201)
    AssertUtils.status_code(result["login_resp"], 200)
    AssertUtils.true(bool(result.get("token")), "login should return token")
