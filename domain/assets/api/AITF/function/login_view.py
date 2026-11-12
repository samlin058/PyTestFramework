from __future__ import annotations

from typing import Any

import allure

from service.http import ApiResponse, HttpClient, authorization_value


class LoginView:
    """LoginView 单接口调用封装（由 api_info/LoginView.yaml 生成）。"""

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.client = http_client or HttpClient(project="AITF")


    @allure.step("接口请求: LoginView.post")
    def post(
        self,
        *,
        account: str = 'admin',
        password: str = '123456',
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 LoginView.post — POST /api/auth/login/。"""
        method = "POST"
        url = "/api/auth/login/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        if json is not None:
            payload = json
        else:
            payload = {}
            if account is not None:
                payload["account"] = account
            if password is not None:
                payload["password"] = password
        return self.client.send(
            method,
            url,
            name="LoginView.post",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )
