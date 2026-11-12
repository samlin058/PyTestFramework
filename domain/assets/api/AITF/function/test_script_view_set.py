from __future__ import annotations

from typing import Any

import allure

from service.http import ApiResponse, HttpClient, authorization_value


class TestScriptViewSet:
    """TestScriptViewSet 单接口调用封装（由 api_info/TestScriptViewSet.yaml 生成）。"""

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.client = http_client or HttpClient(project="AITF")


    @allure.step("接口请求: TestScriptViewSet.list")
    def list(
        self,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 TestScriptViewSet.list — GET /api/scripts/。"""
        method = "GET"
        url = "/api/scripts/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        return self.client.send(
            method,
            url,
            name="TestScriptViewSet.list",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: TestScriptViewSet.create")
    def create(
        self,
        *,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 TestScriptViewSet.create — POST /api/scripts/。"""
        method = "POST"
        url = "/api/scripts/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        return self.client.send(
            method,
            url,
            name="TestScriptViewSet.create",
            json=json,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: TestScriptViewSet.retrieve")
    def retrieve(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 TestScriptViewSet.retrieve — GET /api/scripts/{id}/。"""
        method = "GET"
        url = "/api/scripts/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="TestScriptViewSet.retrieve",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: TestScriptViewSet.update")
    def update(
        self,
        *,
        id_: int | str,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 TestScriptViewSet.update — PUT /api/scripts/{id}/。"""
        method = "PUT"
        url = "/api/scripts/{id}/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="TestScriptViewSet.update",
            json=json,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: TestScriptViewSet.partial_update")
    def partial_update(
        self,
        *,
        id_: int | str,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 TestScriptViewSet.partial_update — PATCH /api/scripts/{id}/。"""
        method = "PATCH"
        url = "/api/scripts/{id}/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="TestScriptViewSet.partial_update",
            json=json,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: TestScriptViewSet.destroy")
    def destroy(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 TestScriptViewSet.destroy — DELETE /api/scripts/{id}/。"""
        method = "DELETE"
        url = "/api/scripts/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="TestScriptViewSet.destroy",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )
