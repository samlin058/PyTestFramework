from __future__ import annotations

from typing import Any

import allure

from service.http import ApiResponse, HttpClient, authorization_value


class UserViewSet:
    """UserViewSet 单接口调用封装（由 api_info/UserViewSet.yaml 生成）。"""

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.client = http_client or HttpClient(project="AITF")


    @allure.step("接口请求: UserViewSet.list")
    def list(
        self,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 UserViewSet.list — GET /api/users/。"""
        method = "GET"
        url = "/api/users/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        return self.client.send(
            method,
            url,
            name="UserViewSet.list",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: UserViewSet.create")
    def create(
        self,
        *,
        account: str | None = None,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        is_staff: bool | None = None,
        is_active: bool | None = None,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 UserViewSet.create — POST /api/users/。"""
        method = "POST"
        url = "/api/users/"
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
            if username is not None:
                payload["username"] = username
            if email is not None:
                payload["email"] = email
            if password is not None:
                payload["password"] = password
            if is_staff is not None:
                payload["is_staff"] = is_staff
            if is_active is not None:
                payload["is_active"] = is_active
        return self.client.send(
            method,
            url,
            name="UserViewSet.create",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: UserViewSet.retrieve")
    def retrieve(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 UserViewSet.retrieve — GET /api/users/{id}/。"""
        method = "GET"
        url = "/api/users/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="UserViewSet.retrieve",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: UserViewSet.update")
    def update(
        self,
        *,
        id_: int | str,
        account: str | None = None,
        username: str | None = None,
        email: str | None = None,
        is_staff: bool | None = None,
        is_active: bool | None = None,
        password: str | None = None,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 UserViewSet.update — PUT /api/users/{id}/。"""
        method = "PUT"
        url = "/api/users/{id}/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        if json is not None:
            payload = json
        else:
            payload = {}
            if account is not None:
                payload["account"] = account
            if username is not None:
                payload["username"] = username
            if email is not None:
                payload["email"] = email
            if is_staff is not None:
                payload["is_staff"] = is_staff
            if is_active is not None:
                payload["is_active"] = is_active
            if password is not None:
                payload["password"] = password
        return self.client.send(
            method,
            url,
            name="UserViewSet.update",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: UserViewSet.partial_update")
    def partial_update(
        self,
        *,
        id_: int | str,
        account: str | None = None,
        username: str | None = None,
        email: str | None = None,
        is_staff: bool | None = None,
        is_active: bool | None = None,
        password: str | None = None,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 UserViewSet.partial_update — PATCH /api/users/{id}/。"""
        method = "PATCH"
        url = "/api/users/{id}/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        if json is not None:
            payload = json
        else:
            payload = {}
            if account is not None:
                payload["account"] = account
            if username is not None:
                payload["username"] = username
            if email is not None:
                payload["email"] = email
            if is_staff is not None:
                payload["is_staff"] = is_staff
            if is_active is not None:
                payload["is_active"] = is_active
            if password is not None:
                payload["password"] = password
        return self.client.send(
            method,
            url,
            name="UserViewSet.partial_update",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: UserViewSet.destroy")
    def destroy(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 UserViewSet.destroy — DELETE /api/users/{id}/。"""
        method = "DELETE"
        url = "/api/users/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="UserViewSet.destroy",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )
