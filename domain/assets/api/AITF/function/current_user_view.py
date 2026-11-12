from __future__ import annotations

from typing import Any

import allure

from service.http import ApiResponse, HttpClient, authorization_value


class CurrentUserView:
    """CurrentUserView 单接口调用封装（由 api_info/CurrentUserView.yaml 生成）。"""

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.client = http_client or HttpClient(project="AITF")


    @allure.step("接口请求: CurrentUserView.get")
    def get(
        self,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 CurrentUserView.get — GET /api/auth/me/。"""
        method = "GET"
        url = "/api/auth/me/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        return self.client.send(
            method,
            url,
            name="CurrentUserView.get",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )
