from __future__ import annotations

import json
from typing import Any

import allure
import requests

from core.config import get_config
from core.http.api_loader import ApiSpecLoader
from core.logger import logger


class HttpClient:
    """HTTP client that resolves interface metadata by controller + url."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int | None = None,
        session: requests.Session | None = None,
        api_loader: ApiSpecLoader | None = None,
    ) -> None:
        """初始化 HTTP 客户端，合并配置中的 base_url、超时与 API 规格加载器。"""
        cfg = get_config()
        self.base_url = (base_url or cfg.get("base_url", "")).rstrip("/")
        self.timeout = timeout if timeout is not None else int(cfg.get("timeout", 10))
        self.session = session or requests.Session()
        self.api_loader = api_loader or ApiSpecLoader()
        self.api_loader.ensure_loaded()

    def request(
        self,
        controller: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | list[Any] | None = None,
        data: Any = None,
        headers: dict[str, str] | None = None,
        path_params: dict[str, Any] | None = None,
        timeout: int | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """按 controller + url 解析接口规格并发送 HTTP 请求，同时记录 Allure 附件。"""
        spec = self.api_loader.get(controller, url)
        method = spec["method"]
        resolved_url = self._resolve_url(spec["url"], path_params)
        merged_headers = {**spec.get("headers", {}), **(headers or {})}
        req_timeout = timeout or spec.get("timeout") or self.timeout

        with allure.step(f"{method} {controller} {spec['url']}"):
            logger.info(f"HTTP {method} {resolved_url} controller={controller}")
            allure.attach(
                self._safe_dump(
                    {
                        "controller": controller,
                        "method": method,
                        "url": resolved_url,
                        "headers": merged_headers,
                        "params": params,
                        "json": json,
                        "data": data,
                    }
                ),
                name="request",
                attachment_type=allure.attachment_type.JSON,
            )
            response = self.session.request(
                method=method,
                url=resolved_url,
                params=params,
                json=json,
                data=data,
                headers=merged_headers,
                timeout=req_timeout,
                **kwargs,
            )
            allure.attach(
                self._safe_dump(
                    {
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "body": self._body_preview(response),
                    }
                ),
                name="response",
                attachment_type=allure.attachment_type.JSON,
            )
            logger.info(f"HTTP <- {response.status_code} {resolved_url}")
            return response

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
