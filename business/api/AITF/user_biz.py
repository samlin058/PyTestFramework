from __future__ import annotations

import allure
import requests

from core.http import HttpClient


class UserBiz:
    CONTROLLER = "UserController"

    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    @allure.step("业务: 用户登录")
    def login(self, email: str, password: str) -> requests.Response:
        return self.client.request(
            self.CONTROLLER,
            "/api/login",
            json={"email": email, "password": password},
        )

    @allure.step("业务: 创建用户")
    def create_user(self, name: str, job: str) -> requests.Response:
        return self.client.request(
            self.CONTROLLER,
            "/api/users",
            json={"name": name, "job": job},
        )

    @allure.step("业务: 查询用户")
    def get_user(self, user_id: int | str) -> requests.Response:
        return self.client.request(
            self.CONTROLLER,
            "/api/users/{id}",
            path_params={"id": user_id},
        )
