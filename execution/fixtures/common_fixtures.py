from __future__ import annotations

from typing import Any

import pytest

from core.config import get_config, get_project_config, resolve_project_name
from core.database import DatabaseClient
from datafactory.api.AITF.user_factory import UserDataFactory


@pytest.fixture
def project_name(request: pytest.FixtureRequest) -> str:
    """从当前用例路径解析项目名（testCases/<api|ui>/<project>/...）。"""
    return resolve_project_name(request.path)


@pytest.fixture
def project_config(project_name: str) -> dict[str, Any]:
    """返回当前用例所属项目的合并配置。"""
    return get_project_config(project_name)


@pytest.fixture(scope="session")
def env_config() -> dict[str, Any]:
    """返回当前环境完整配置（含 defaults / projects）。"""
    return get_config()


@pytest.fixture(scope="session")
def _db_clients() -> dict[str, DatabaseClient]:
    """按项目缓存 DatabaseClient，会话结束统一关闭。"""
    clients: dict[str, DatabaseClient] = {}
    yield clients
    for client in clients.values():
        client.close()


@pytest.fixture
def db(project_name: str, project_config: dict[str, Any], _db_clients: dict[str, DatabaseClient]):
    """按项目获取数据库客户端；未启用时为 no-op。"""
    if project_name not in _db_clients:
        client = DatabaseClient(project_config.get("db"))
        if client.enabled:
            client.connect()
        _db_clients[project_name] = client
    return _db_clients[project_name]


@pytest.fixture
def user_factory(http_client, db) -> UserDataFactory:
    return UserDataFactory(http_client=http_client, db=db)
