from __future__ import annotations

from typing import Any

import pytest

from service.http import HttpClient


@pytest.fixture(scope="session")
def _http_clients() -> dict[str, HttpClient]:
    """按项目缓存 HttpClient。"""
    return {}


@pytest.fixture
def http_client(
    project_name: str,
    project_config: dict[str, Any],
    _http_clients: dict[str, HttpClient],
) -> HttpClient:
    """按当前用例所属项目返回 HttpClient。"""
    if project_name not in _http_clients:
        _http_clients[project_name] = HttpClient(
            project=project_name,
            base_url=project_config.get("api_base_url"),
            timeout=project_config.get("timeout"),
        )
    return _http_clients[project_name]
