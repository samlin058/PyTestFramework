from typing import Any

import allure

from business.api.AITF.user_biz import UserBiz
from core.database import DatabaseClient
from core.http import HttpClient
from core.logger import logger
from datafactory.db.user_db_factory import UserDbFactory


class UserDataFactory:
    """造数工厂：单接口直调 HttpClient；复杂前置复用 business 场景。"""

    CONTROLLER = "UserController"

    def __init__(self, http_client: HttpClient, db: DatabaseClient | None = None) -> None:
        self.client = http_client
        self.biz = UserBiz(http_client, db=db)
        self.db_factory = UserDbFactory(db) if db else None

    @allure.step("造数: 通过单接口创建用户")
    def create_user(self, name: str = "auto_user", job: str = "tester") -> dict[str, Any]:
        resp = self.client.call(
            self.CONTROLLER,
            "createUser",
            json={"name": name, "job": job},
        )
        user = resp.json()
        logger.info(f"Created user via API: {user}")
        return user

    @allure.step("造数: 通过业务场景登录并查询用户")
    def login_and_get_user(
        self,
        *,
        email: str | None = None,
        password: str | None = None,
        user_id: int | str = 2,
    ) -> dict[str, Any]:
        account = self.prepare_login_account()
        return self.biz.login_and_get_user(
            email=email or account["email"],
            password=password or account["password"],
            user_id=user_id,
        )

    @allure.step("造数: 通过数据库插入用户（需开启 db.enabled）")
    def insert_user_row(self, name: str, email: str) -> dict[str, Any]:
        if not self.db_factory:
            raise RuntimeError("Database client is not available")
        return self.db_factory.insert_user(name=name, email=email)

    @allure.step("造数: 准备可登录账号数据")
    def prepare_login_account(self) -> dict[str, str]:
        """Return a known-valid reqres account for demo login."""
        return {"email": "eve.holt@reqres.in", "password": "cityslicka"}
