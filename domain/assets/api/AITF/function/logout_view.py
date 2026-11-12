from __future__ import annotations

from typing import Any

import allure

from service.http import ApiResponse, HttpClient, authorization_value


class LogoutView:
    """LogoutView 单接口调用封装（由 api_info/LogoutView.yaml 生成）。"""

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.client = http_client or HttpClient(project="AITF")


    @allure.step("接口请求: LogoutView.post")
    def post(
        self,
        *,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 LogoutView.post — POST /api/auth/logout/。"""
        method = "POST"
        url = "/api/auth/logout/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        return self.client.send(
            method,
            url,
            name="LogoutView.post",
            json=json,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )
