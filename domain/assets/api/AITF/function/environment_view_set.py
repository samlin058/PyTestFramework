from __future__ import annotations

from typing import Any

import allure

from service.http import ApiResponse, HttpClient, authorization_value


class EnvironmentViewSet:
    """EnvironmentViewSet 单接口调用封装（由 api_info/EnvironmentViewSet.yaml 生成）。"""

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.client = http_client or HttpClient(project="AITF")


    @allure.step("接口请求: EnvironmentViewSet.list")
    def list(
        self,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 EnvironmentViewSet.list — GET /api/environments/。"""
        method = "GET"
        url = "/api/environments/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        return self.client.send(
            method,
            url,
            name="EnvironmentViewSet.list",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: EnvironmentViewSet.create")
    def create(
        self,
        *,
        name: str | None = None,
        config_path: str | None = None,
        base_url: str | None = None,
        variables: dict[str, Any] | None = None,
        is_active: bool = True,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 EnvironmentViewSet.create — POST /api/environments/。"""
        method = "POST"
        url = "/api/environments/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        if json is not None:
            payload = json
        else:
            payload = {}
            if name is not None:
                payload["name"] = name
            if config_path is not None:
                payload["config_path"] = config_path
            if base_url is not None:
                payload["base_url"] = base_url
            if variables is not None:
                payload["variables"] = variables
            if is_active is not None:
                payload["is_active"] = is_active
        return self.client.send(
            method,
            url,
            name="EnvironmentViewSet.create",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: EnvironmentViewSet.retrieve")
    def retrieve(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 EnvironmentViewSet.retrieve — GET /api/environments/{id}/。"""
        method = "GET"
        url = "/api/environments/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="EnvironmentViewSet.retrieve",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: EnvironmentViewSet.update")
    def update(
        self,
        *,
        id_: int | str,
        name: str | None = None,
        config_path: str | None = None,
        base_url: str | None = None,
        variables: dict[str, Any] | None = None,
        is_active: bool = True,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 EnvironmentViewSet.update — PUT /api/environments/{id}/。"""
        method = "PUT"
        url = "/api/environments/{id}/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        if json is not None:
            payload = json
        else:
            payload = {}
            if name is not None:
                payload["name"] = name
            if config_path is not None:
                payload["config_path"] = config_path
            if base_url is not None:
                payload["base_url"] = base_url
            if variables is not None:
                payload["variables"] = variables
            if is_active is not None:
                payload["is_active"] = is_active
        return self.client.send(
            method,
            url,
            name="EnvironmentViewSet.update",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: EnvironmentViewSet.partial_update")
    def partial_update(
        self,
        *,
        id_: int | str,
        name: str | None = None,
        config_path: str | None = None,
        base_url: str | None = None,
        variables: dict[str, Any] | None = None,
        is_active: bool = True,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 EnvironmentViewSet.partial_update — PATCH /api/environments/{id}/。"""
        method = "PATCH"
        url = "/api/environments/{id}/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        if json is not None:
            payload = json
        else:
            payload = {}
            if name is not None:
                payload["name"] = name
            if config_path is not None:
                payload["config_path"] = config_path
            if base_url is not None:
                payload["base_url"] = base_url
            if variables is not None:
                payload["variables"] = variables
            if is_active is not None:
                payload["is_active"] = is_active
        return self.client.send(
            method,
            url,
            name="EnvironmentViewSet.partial_update",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: EnvironmentViewSet.destroy")
    def destroy(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 EnvironmentViewSet.destroy — DELETE /api/environments/{id}/。"""
        method = "DELETE"
        url = "/api/environments/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="EnvironmentViewSet.destroy",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )
