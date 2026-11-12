from __future__ import annotations

import json
from typing import Any

import allure
import requests

from service.config import get_project_config
from service.http.response import ApiResponse
from service.logger import logger


class HttpClient:
    """HTTP client that sends requests with project base_url / timeout."""

    def __init__(
        self,
        project: str,
        base_url: str | None = None,
        timeout: int | None = None,
        session: requests.Session | None = None,
    ) -> None:
        """初始化 HTTP 客户端：按项目读取 api_base_url / 超时。"""
        cfg = get_project_config(project)
        self.project = project
        self.base_url = (base_url or cfg.get("api_base_url", "")).rstrip("/")
        self.timeout = timeout if timeout is not None else int(cfg.get("timeout", 10))
        self.session = session or requests.Session()

    def send(
        self,
        method: str,
        url: str,
        *,
        name: str | None = None,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | list[Any] | None = None,
        data: Any = None,
        headers: dict[str, str] | None = None,
        path_params: dict[str, Any] | None = None,
        timeout: int | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """直传 method/url/headers 发起请求。"""
        api_method = str(method).upper()
        api_name = name or url
        resolved_url = self._resolve_url(url, path_params)
        req_headers = dict(headers or {})
        req_timeout = timeout if timeout is not None else self.timeout

        with allure.step(f"{api_method} {api_name} {url}"):
            request_payload = {
                "project": self.project,
                "name": api_name,
                "method": api_method,
                "url": resolved_url,
                "headers": req_headers,
                "params": params,
                "path_params": path_params,
                "json": json,
                "data": data,
            }
            self._log_request(
                method=api_method,
                url=resolved_url,
                headers=req_headers,
                params=params,
                path_params=path_params,
                json_body=json,
                data=data,
            )
            allure.attach(
                self._safe_dump(request_payload),
                name="request",
                attachment_type=allure.attachment_type.JSON,
            )
            response = self.session.request(
                method=api_method,
                url=resolved_url,
                params=params,
                json=json,
                data=data,
                headers=req_headers,
                timeout=req_timeout,
                **kwargs,
            )
            return self._finalize_response(response)

    def _finalize_response(self, response: requests.Response) -> ApiResponse:
        """将 Response 转为 ApiResponse，并记录 Allure / 日志。"""
        body = self._body_preview(response)
        result = ApiResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            body=body,
        )
        allure.attach(
            self._safe_dump(
                {
                    "status_code": result.status_code,
                    "headers": result.headers,
                    "body": result.body,
                }
            ),
            name="response",
            attachment_type=allure.attachment_type.JSON,
        )
        self._log_response(response)
        return result

    def _resolve_url(self, url: str, path_params: dict[str, Any] | None) -> str:
        """替换路径参数并拼接 base_url，得到最终请求地址。"""
        path = url
        if path_params:
            for key, value in path_params.items():
                path = path.replace("{" + str(key) + "}", str(value))
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self.base_url}{path if path.startswith('/') else '/' + path}"

    @staticmethod
    def _log_request(
        *,
        method: str,
        url: str,
        headers: dict[str, str] | None,
        params: dict[str, Any] | None,
        path_params: dict[str, Any] | None,
        json_body: dict[str, Any] | list[Any] | None,
        data: Any,
    ) -> None:
        """打印通用请求日志：路径、请求头（如有）、请求参数。"""
        logger.info(f"请求路径: {method} {url}")
        if headers:
            logger.info(f"请求头: {HttpClient._safe_dump(headers)}")
        request_args: dict[str, Any] = {}
        if path_params:
            request_args["path_params"] = path_params
        if params:
            request_args["params"] = params
        if json_body is not None:
            request_args["json"] = json_body
        if data is not None:
            request_args["data"] = data
        if request_args:
            logger.info(f"请求参数: {HttpClient._safe_dump(request_args)}")

    @staticmethod
    def _log_response(response: requests.Response) -> None:
        """打印通用响应日志：状态码与返回体。"""
        logger.info(
            f"返回体: status={response.status_code} "
            f"body={HttpClient._safe_dump(HttpClient._body_preview(response))}"
        )

    @staticmethod
    def _body_preview(response: requests.Response) -> Any:
        """提取响应体预览：优先 JSON，否则截取文本前 2000 字符。"""
        try:
            return response.json()
        except Exception:
            text = response.text or ""
            return text[:2000]

    @staticmethod
    def _safe_dump(payload: Any) -> str:
        """将对象安全序列化为 JSON 字符串，失败时回退为 str。"""
        try:
            return json.dumps(payload, ensure_ascii=False, indent=2, default=str)
        except Exception:
            return str(payload)
