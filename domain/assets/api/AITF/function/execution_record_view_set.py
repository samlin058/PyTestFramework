from __future__ import annotations

from typing import Any

import allure

from service.http import ApiResponse, HttpClient, authorization_value


class ExecutionRecordViewSet:
    """ExecutionRecordViewSet 单接口调用封装（由 api_info/ExecutionRecordViewSet.yaml 生成）。"""

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.client = http_client or HttpClient(project="AITF")


    @allure.step("接口请求: ExecutionRecordViewSet.list")
    def list(
        self,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ExecutionRecordViewSet.list — GET /api/execution-records/。"""
        method = "GET"
        url = "/api/execution-records/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        return self.client.send(
            method,
            url,
            name="ExecutionRecordViewSet.list",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: ExecutionRecordViewSet.retrieve")
    def retrieve(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 ExecutionRecordViewSet.retrieve — GET /api/execution-records/{id}/。"""
        method = "GET"
        url = "/api/execution-records/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="ExecutionRecordViewSet.retrieve",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )
