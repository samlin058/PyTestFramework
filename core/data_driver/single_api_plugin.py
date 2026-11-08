from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from core.config import get_project_config
from core.data_driver.single_api_case_loader import is_single_api_yaml, load_single_api_file
from core.data_driver.single_api_runner import run_single_api_case
from core.database import DatabaseClient
from core.http import HttpClient
from core.http.api_loader import ApiSpecLoader

_api_loader = ApiSpecLoader()
_http_clients: dict[str, HttpClient] = {}
_db_clients: dict[str, DatabaseClient] = {}


def pytest_collect_file(file_path: Path, parent: pytest.Collector):
    """收集 testCases/api/<project>/single/*.yaml 为单接口用例。"""
    if not is_single_api_yaml(file_path):
        return None
    return SingleApiFile.from_parent(parent, path=file_path)


class SingleApiFile(pytest.File):
    """一份单接口 YAML 文件对应的收集节点。"""

    def collect(self):
        units = load_single_api_file(self.path, api_loader=_api_loader)
        for unit in units:
            case = unit["case"]
            case_id = case.get("case_id") or f"case_{unit['case_index']}"
            name = str(case_id)
            yield SingleApiItem.from_parent(self, name=name, unit=unit)


class SingleApiItem(pytest.Item):
    """单条 case 对应的执行节点。"""

    def __init__(self, name: str, parent: pytest.Collector, unit: dict[str, Any], **kwargs: Any):
        super().__init__(name, parent, **kwargs)
        self.unit = unit
        self.add_marker(pytest.mark.api)

    def runtest(self) -> None:
        __tracebackhide__ = True
        project = self.unit["project"]
        http_client = _get_http_client(project)
        db = _get_db_client(project)
        run_single_api_case(self.unit, http_client=http_client, db=db)

    def repr_failure(self, excinfo) -> str:
        """压缩单接口失败输出，避免打出 pytest/pluggy 整段堆栈。"""
        if isinstance(excinfo.value, AssertionError):
            return f"AssertionError: {excinfo.value}"
        return f"{excinfo.type.__name__}: {excinfo.value}"

    def reportinfo(self):
        case = self.unit.get("case") or {}
        label = case.get("name") or case.get("case_id") or self.name
        return self.path, None, f"single_api: {label}"


def _get_http_client(project: str) -> HttpClient:
    if project not in _http_clients:
        cfg = get_project_config(project)
        _http_clients[project] = HttpClient(
            project=project,
            base_url=cfg.get("api_base_url"),
            timeout=cfg.get("timeout"),
            api_loader=_api_loader,
        )
    return _http_clients[project]


def _get_db_client(project: str) -> DatabaseClient:
    if project not in _db_clients:
        cfg = get_project_config(project)
        client = DatabaseClient(cfg.get("db"))
        if client.enabled:
            client.connect()
        _db_clients[project] = client
    return _db_clients[project]


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:  # noqa: ARG001
    """会话结束关闭插件内缓存的 DB 连接。"""
    for client in _db_clients.values():
        client.close()
    _db_clients.clear()
