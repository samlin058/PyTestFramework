from __future__ import annotations

from typing import Any


class ApiResponse(dict):
    """接口响应：行为像业务 JSON 字典，另挂 status_code / headers / body。

    - 响应体是对象时：可直接 ``resp["token"]``、``resp.get("id")``
    - HTTP 状态码：``resp.status_code``
    - 原始响应体（含 list/str）：``resp.body``
    """

    __slots__ = ("status_code", "headers", "body")

    def __init__(
        self,
        status_code: int,
        headers: dict[str, str] | None,
        body: Any,
    ) -> None:
        self.status_code = status_code
        self.headers = dict(headers or {})
        self.body = body
        if isinstance(body, dict):
            super().__init__(body)
        else:
            super().__init__()

    def __repr__(self) -> str:
        return (
            f"ApiResponse(status_code={self.status_code!r}, "
            f"body={self.body!r})"
        )
