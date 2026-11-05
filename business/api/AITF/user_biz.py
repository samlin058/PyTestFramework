from __future__ import annotations

from typing import Any

import allure

from core.database import DatabaseClient
from core.http import HttpClient
from core.logger import logger


class UserBiz:
    """用户相关业务场景编排（多接口串联 / 可选 DB），不做断言。"""

    CONTROLLER = "UserController"

    def __init__(
        self,
        http_client: HttpClient,
        db: DatabaseClient | None = None,
    ) -> None:
        self.client = http_client
        self.db = db

    @allure.step("业务场景: 登录后查询用户")
    def login_and_get_user(
        self,
        *,
        email: str,
        password: str,
        user_id: int | str = 2,
    ) -> dict[str, Any]:
        """先登录拿 token，再查询指定用户，返回可复用上下文。"""
        login_resp = self.client.call(
            self.CONTROLLER,
            "login",
            json={"email": email, "password": password},
        )
        login_body = login_resp.json()

        get_resp = self.client.call(
            self.CONTROLLER,
            "getUser",
            path_params={"id": user_id},
        )
        result = {
            "login_resp": login_resp,
            "token": login_body.get("token"),
            "get_resp": get_resp,
            "user": get_resp.json(),
            "email": email,
        }
        logger.info(
            f"login_and_get_user done: user_id={user_id} "
            f"token_present={bool(result['token'])}"
        )
        return result

    @allure.step("业务场景: 创建用户后登录")
    def create_user_then_login(
        self,
        *,
        name: str,
        job: str,
        email: str,
        password: str,
    ) -> dict[str, Any]:
        """先创建用户，再登录拿 token，组装可复用的业务上下文。"""
        create_resp = self.client.call(
            self.CONTROLLER,
            "createUser",
            json={"name": name, "job": job},
        )
        created = create_resp.json()

        login_resp = self.client.call(
            self.CONTROLLER,
            "login",
            json={"email": email, "password": password},
        )
        login_body = login_resp.json()
        result = {
            "create_resp": create_resp,
            "created": created,
            "login_resp": login_resp,
            "token": login_body.get("token"),
            "email": email,
        }
        logger.info(
            f"create_user_then_login done: user_id={created.get('id')} "
            f"token_present={bool(result['token'])}"
        )
        return result

    @allure.step("业务场景: DB 落库用户后走接口登录（需开启 db.enabled）")
    def seed_db_user_and_login(
        self,
        *,
        name: str,
        email: str,
        password: str,
    ) -> dict[str, Any]:
        """DB 插入用户后调用登录接口，演示 API + DB 混合编排。"""
        if not self.db or not self.db.enabled:
            raise RuntimeError("Database client is not available (db.enabled=false)")

        self.db.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (name, email),
        )
        row = self.db.fetch_one(
            "SELECT * FROM users WHERE email=%s ORDER BY id DESC LIMIT 1",
            (email,),
        )
        login_resp = self.client.call(
            self.CONTROLLER,
            "login",
            json={"email": email, "password": password},
        )
        login_body = login_resp.json()
        return {
            "db_user": row or {"name": name, "email": email},
            "login_resp": login_resp,
            "token": login_body.get("token"),
        }
