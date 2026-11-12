from __future__ import annotations

from typing import Any

import allure

from service.http import ApiResponse, HttpClient, authorization_value


class ProjectViewSet:
    """ProjectViewSet 单接口调用封装（由 api_info/ProjectViewSet.yaml 生成）。"""

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.client = http_client or HttpClient(project="AITF")


    @allure.step("接口请求: ProjectViewSet.list")
    def list(
        self,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ProjectViewSet.list — GET /api/projects/。"""
        method = "GET"
        url = "/api/projects/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        return self.client.send(
            method,
            url,
            name="ProjectViewSet.list",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ProjectViewSet.create")
    def create(
        self,
        *,
        name: str | None = None,
        code: str | None = None,
        description: str | None = None,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ProjectViewSet.create — POST /api/projects/。"""
        method = "POST"
        url = "/api/projects/"
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
            if code is not None:
                payload["code"] = code
            if description is not None:
                payload["description"] = description
        return self.client.send(
            method,
            url,
            name="ProjectViewSet.create",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ProjectViewSet.retrieve")
    def retrieve(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ProjectViewSet.retrieve — GET /api/projects/{id}/。"""
        method = "GET"
        url = "/api/projects/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="ProjectViewSet.retrieve",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ProjectViewSet.update")
    def update(
        self,
        *,
        id_: int | str,
        name: str | None = None,
        code: str | None = None,
        description: str | None = None,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ProjectViewSet.update — PUT /api/projects/{id}/。"""
        method = "PUT"
        url = "/api/projects/{id}/"
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
            if code is not None:
                payload["code"] = code
            if description is not None:
                payload["description"] = description
        return self.client.send(
            method,
            url,
            name="ProjectViewSet.update",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ProjectViewSet.partial_update")
    def partial_update(
        self,
        *,
        id_: int | str,
        name: str | None = None,
        code: str | None = None,
        description: str | None = None,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ProjectViewSet.partial_update — PATCH /api/projects/{id}/。"""
        method = "PATCH"
        url = "/api/projects/{id}/"
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
            if code is not None:
                payload["code"] = code
            if description is not None:
                payload["description"] = description
        return self.client.send(
            method,
            url,
            name="ProjectViewSet.partial_update",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ProjectViewSet.destroy")
    def destroy(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ProjectViewSet.destroy — DELETE /api/projects/{id}/。"""
        method = "DELETE"
        url = "/api/projects/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="ProjectViewSet.destroy",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )
