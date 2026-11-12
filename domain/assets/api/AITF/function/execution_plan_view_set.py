from __future__ import annotations

from typing import Any

import allure

from service.http import ApiResponse, HttpClient, authorization_value


class ExecutionPlanViewSet:
    """ExecutionPlanViewSet 单接口调用封装（由 api_info/ExecutionPlanViewSet.yaml 生成）。"""

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.client = http_client or HttpClient(project="AITF")


    @allure.step("接口请求: ExecutionPlanViewSet.list")
    def list(
        self,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ExecutionPlanViewSet.list — GET /api/execution-plans/。"""
        method = "GET"
        url = "/api/execution-plans/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        return self.client.send(
            method,
            url,
            name="ExecutionPlanViewSet.list",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ExecutionPlanViewSet.create")
    def create(
        self,
        *,
        environment: int | None = None,
        name: str | None = None,
        plan_type: str | None = None,
        jenkins_job_name: str | None = None,
        case_dir: str | None = None,
        case_tags: list[Any] | None = None,
        pytest_args: list[Any] | None = None,
        is_active: bool = True,
        script_ids: list[Any] | None = None,
        schedule: dict[str, Any] | None = None,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ExecutionPlanViewSet.create — POST /api/execution-plans/。"""
        method = "POST"
        url = "/api/execution-plans/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        if json is not None:
            payload = json
        else:
            payload = {}
            if environment is not None:
                payload["environment"] = environment
            if name is not None:
                payload["name"] = name
            if plan_type is not None:
                payload["plan_type"] = plan_type
            if jenkins_job_name is not None:
                payload["jenkins_job_name"] = jenkins_job_name
            if case_dir is not None:
                payload["case_dir"] = case_dir
            if case_tags is not None:
                payload["case_tags"] = case_tags
            if pytest_args is not None:
                payload["pytest_args"] = pytest_args
            if is_active is not None:
                payload["is_active"] = is_active
            if script_ids is not None:
                payload["script_ids"] = script_ids
            if schedule is not None:
                payload["schedule"] = schedule
        return self.client.send(
            method,
            url,
            name="ExecutionPlanViewSet.create",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ExecutionPlanViewSet.retrieve")
    def retrieve(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ExecutionPlanViewSet.retrieve — GET /api/execution-plans/{id}/。"""
        method = "GET"
        url = "/api/execution-plans/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="ExecutionPlanViewSet.retrieve",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ExecutionPlanViewSet.update")
    def update(
        self,
        *,
        id_: int | str,
        environment: int | None = None,
        name: str | None = None,
        plan_type: str | None = None,
        jenkins_job_name: str | None = None,
        case_dir: str | None = None,
        case_tags: list[Any] | None = None,
        pytest_args: list[Any] | None = None,
        is_active: bool = True,
        script_ids: list[Any] | None = None,
        schedule: dict[str, Any] | None = None,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ExecutionPlanViewSet.update — PUT /api/execution-plans/{id}/。"""
        method = "PUT"
        url = "/api/execution-plans/{id}/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        if json is not None:
            payload = json
        else:
            payload = {}
            if environment is not None:
                payload["environment"] = environment
            if name is not None:
                payload["name"] = name
            if plan_type is not None:
                payload["plan_type"] = plan_type
            if jenkins_job_name is not None:
                payload["jenkins_job_name"] = jenkins_job_name
            if case_dir is not None:
                payload["case_dir"] = case_dir
            if case_tags is not None:
                payload["case_tags"] = case_tags
            if pytest_args is not None:
                payload["pytest_args"] = pytest_args
            if is_active is not None:
                payload["is_active"] = is_active
            if script_ids is not None:
                payload["script_ids"] = script_ids
            if schedule is not None:
                payload["schedule"] = schedule
        return self.client.send(
            method,
            url,
            name="ExecutionPlanViewSet.update",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ExecutionPlanViewSet.partial_update")
    def partial_update(
        self,
        *,
        id_: int | str,
        environment: int | None = None,
        name: str | None = None,
        plan_type: str | None = None,
        jenkins_job_name: str | None = None,
        case_dir: str | None = None,
        case_tags: list[Any] | None = None,
        pytest_args: list[Any] | None = None,
        is_active: bool = True,
        script_ids: list[Any] | None = None,
        schedule: dict[str, Any] | None = None,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ExecutionPlanViewSet.partial_update — PATCH /api/execution-plans/{id}/。"""
        method = "PATCH"
        url = "/api/execution-plans/{id}/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        if json is not None:
            payload = json
        else:
            payload = {}
            if environment is not None:
                payload["environment"] = environment
            if name is not None:
                payload["name"] = name
            if plan_type is not None:
                payload["plan_type"] = plan_type
            if jenkins_job_name is not None:
                payload["jenkins_job_name"] = jenkins_job_name
            if case_dir is not None:
                payload["case_dir"] = case_dir
            if case_tags is not None:
                payload["case_tags"] = case_tags
            if pytest_args is not None:
                payload["pytest_args"] = pytest_args
            if is_active is not None:
                payload["is_active"] = is_active
            if script_ids is not None:
                payload["script_ids"] = script_ids
            if schedule is not None:
                payload["schedule"] = schedule
        return self.client.send(
            method,
            url,
            name="ExecutionPlanViewSet.partial_update",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ExecutionPlanViewSet.destroy")
    def destroy(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ExecutionPlanViewSet.destroy — DELETE /api/execution-plans/{id}/。"""
        method = "DELETE"
        url = "/api/execution-plans/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="ExecutionPlanViewSet.destroy",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ExecutionPlanViewSet.trigger")
    def trigger(
        self,
        *,
        id_: int | str,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ExecutionPlanViewSet.trigger — POST /api/execution-plans/{id}/trigger/。"""
        method = "POST"
        url = "/api/execution-plans/{id}/trigger/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="ExecutionPlanViewSet.trigger",
            json=json,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ExecutionPlanViewSet.records")
    def records(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ExecutionPlanViewSet.records — GET /api/execution-plans/{id}/records/。"""
        method = "GET"
        url = "/api/execution-plans/{id}/records/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="ExecutionPlanViewSet.records",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )
