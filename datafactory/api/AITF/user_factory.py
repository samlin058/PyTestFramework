from __future__ import annotations

from typing import Any

import allure

from business.api.AITF.user_biz import UserBiz
from core.database import DatabaseClient
from core.http import HttpClient
from core.logger import logger
from datafactory.db.user_db_factory import UserDbFactory


class UserDataFactory:
    """Create users via business layer or DB for test prerequisites."""

    def __init__(self, http_client: HttpClient, db: DatabaseClient | None = None) -> None:
        self.biz = UserBiz(http_client)
        self.db_factory = UserDbFactory(db) if db else None

    @allure.step("造数: 通过业务接口创建用户")
    def create_user(self, name: str = "auto_user", job: str = "tester") -> dict[str, Any]:
        resp = self.biz.create_user(name=name, job=job)
        user = resp.json()
        logger.info(f"Created user via API: {user}")
        return user

    @allure.step("造数: 通过数据库插入用户（需开启 db.enabled）")
    def insert_user_row(self, name: str, email: str) -> dict[str, Any]:
        if not self.db_factory:
            raise RuntimeError("Database client is not available")
        return self.db_factory.insert_user(name=name, email=email)

    @allure.step("造数: 准备可登录账号数据")
    def prepare_login_account(self) -> dict[str, str]:
        """Return a known-valid reqres account for demo login."""
        return {"email": "eve.holt@reqres.in", "password": "cityslicka"}
