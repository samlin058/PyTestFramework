from __future__ import annotations

from typing import Any

import allure

from service.http import ApiResponse, HttpClient, authorization_value


class JenkinsWebhookView:
    """JenkinsWebhookView 单接口调用封装（由 api_info/JenkinsWebhookView.yaml 生成）。"""

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.client = http_client or HttpClient(project="AITF")


    @allure.step("接口请求: JenkinsWebhookView.post")
    def post(
        self,
        *,
        execution_record_id: int | None = None,
        AITF_EXECUTION_RECORD_ID: int | None = None,
        event_type: str | None = None,
        status: str | None = None,
        job_name: str | None = None,
        name: str | None = None,
        build_number: int | None = None,
        build_url: str | None = None,
        report_url: str | None = None,
        report_path: str | None = None,
        summary: dict[str, Any] | None = None,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 JenkinsWebhookView.post — POST /api/integrations/jenkins/webhook/。"""
        method = "POST"
        url = "/api/integrations/jenkins/webhook/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        if json is not None:
            payload = json
        else:
            payload = {}
            if execution_record_id is not None:
                payload["execution_record_id"] = execution_record_id
            if AITF_EXECUTION_RECORD_ID is not None:
                payload["AITF_EXECUTION_RECORD_ID"] = AITF_EXECUTION_RECORD_ID
            if event_type is not None:
                payload["event_type"] = event_type
            if status is not None:
                payload["status"] = status
            if job_name is not None:
                payload["job_name"] = job_name
            if name is not None:
                payload["name"] = name
            if build_number is not None:
                payload["build_number"] = build_number
            if build_url is not None:
                payload["build_url"] = build_url
            if report_url is not None:
                payload["report_url"] = report_url
            if report_path is not None:
                payload["report_path"] = report_path
            if summary is not None:
                payload["summary"] = summary
        return self.client.send(
            method,
            url,
            name="JenkinsWebhookView.post",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )
