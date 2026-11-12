from __future__ import annotations

from typing import Any

import allure

from service.http import ApiResponse, HttpClient, authorization_value


class ScheduleViewSet:
    """ScheduleViewSet 单接口调用封装（由 api_info/ScheduleViewSet.yaml 生成）。"""

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.client = http_client or HttpClient(project="AITF")


    @allure.step("接口请求: ScheduleViewSet.list")
    def list(
        self,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ScheduleViewSet.list — GET /api/schedules/。"""
        method = "GET"
        url = "/api/schedules/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        return self.client.send(
            method,
            url,
            name="ScheduleViewSet.list",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ScheduleViewSet.create")
    def create(
        self,
        *,
        execution_plan: int | None = None,
        name: str | None = None,
        schedule_type: str = 'cron',
        cron_expression: str | None = None,
        interval_seconds: int | None = None,
        is_active: bool = True,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ScheduleViewSet.create — POST /api/schedules/。"""
        method = "POST"
        url = "/api/schedules/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        if json is not None:
            payload = json
        else:
            payload = {}
            if execution_plan is not None:
                payload["execution_plan"] = execution_plan
            if name is not None:
                payload["name"] = name
            if schedule_type is not None:
                payload["schedule_type"] = schedule_type
            if cron_expression is not None:
                payload["cron_expression"] = cron_expression
            if interval_seconds is not None:
                payload["interval_seconds"] = interval_seconds
            if is_active is not None:
                payload["is_active"] = is_active
        return self.client.send(
            method,
            url,
            name="ScheduleViewSet.create",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ScheduleViewSet.retrieve")
    def retrieve(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ScheduleViewSet.retrieve — GET /api/schedules/{id}/。"""
        method = "GET"
        url = "/api/schedules/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="ScheduleViewSet.retrieve",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ScheduleViewSet.update")
    def update(
        self,
        *,
        id_: int | str,
        execution_plan: int | None = None,
        name: str | None = None,
        schedule_type: str = 'cron',
        cron_expression: str | None = None,
        interval_seconds: int | None = None,
        is_active: bool = True,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ScheduleViewSet.update — PUT /api/schedules/{id}/。"""
        method = "PUT"
        url = "/api/schedules/{id}/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        if json is not None:
            payload = json
        else:
            payload = {}
            if execution_plan is not None:
                payload["execution_plan"] = execution_plan
            if name is not None:
                payload["name"] = name
            if schedule_type is not None:
                payload["schedule_type"] = schedule_type
            if cron_expression is not None:
                payload["cron_expression"] = cron_expression
            if interval_seconds is not None:
                payload["interval_seconds"] = interval_seconds
            if is_active is not None:
                payload["is_active"] = is_active
        return self.client.send(
            method,
            url,
            name="ScheduleViewSet.update",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ScheduleViewSet.partial_update")
    def partial_update(
        self,
        *,
        id_: int | str,
        execution_plan: int | None = None,
        name: str | None = None,
        schedule_type: str = 'cron',
        cron_expression: str | None = None,
        interval_seconds: int | None = None,
        is_active: bool = True,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ScheduleViewSet.partial_update — PATCH /api/schedules/{id}/。"""
        method = "PATCH"
        url = "/api/schedules/{id}/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        if json is not None:
            payload = json
        else:
            payload = {}
            if execution_plan is not None:
                payload["execution_plan"] = execution_plan
            if name is not None:
                payload["name"] = name
            if schedule_type is not None:
                payload["schedule_type"] = schedule_type
            if cron_expression is not None:
                payload["cron_expression"] = cron_expression
            if interval_seconds is not None:
                payload["interval_seconds"] = interval_seconds
            if is_active is not None:
                payload["is_active"] = is_active
        return self.client.send(
            method,
            url,
            name="ScheduleViewSet.partial_update",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ScheduleViewSet.destroy")
    def destroy(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ScheduleViewSet.destroy — DELETE /api/schedules/{id}/。"""
        method = "DELETE"
        url = "/api/schedules/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="ScheduleViewSet.destroy",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )
