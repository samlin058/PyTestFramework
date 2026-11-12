from __future__ import annotations

import inspect
import json
import re
from pathlib import Path
from typing import Any

import yaml

from service.data_driver.placeholder import resolve_placeholders, resolve_project_from_path
from service.utils.path_util import PROJECT_ROOT, resolve_path

# YAML 会把未加引号的 ``{{...}}`` / ``@{...}`` 当成 flow mapping / 非法 token；
# 加载前先换成临时 token，解析后再还原，这样无参写法无需加 ``()`` 或引号。
_YAML_PLACEHOLDER = re.compile(r"(\{\{[^{}]+\}\}|@\{[^}]+\}|\$\{[^}]+\})")
_YAML_SHIELD_PREFIX = "__PH_SHIELD_"


def _caller_dir() -> Path | None:
    """定位调用方模块所在目录（跳过 data_driver 自身）。"""
    frame = inspect.currentframe()
    try:
        while frame is not None:
            frame = frame.f_back
            if frame is None:
                break
            filename = frame.f_code.co_filename
            if filename.startswith("<"):
                continue
            path = Path(filename).resolve()
            if "data_driver" in path.parts:
                continue
            return path.parent
    finally:
        del frame
    return None


def _resolve(path: str | Path) -> Path:
    """解析数据文件路径。

    - 绝对路径：直接使用
    - 仅文件名（如 user.yaml）：优先取调用方同级 data/<文件名>
    - 其它相对路径：项目根 → application/testCases/<path>
    """
    p = Path(path)
    if p.is_absolute():
        return p

    if len(p.parts) == 1:
        caller = _caller_dir()
        if caller is not None:
            return caller / "data" / p.name

    candidate = resolve_path(path)
    if candidate.exists():
        return candidate
    return PROJECT_ROOT / "application" / "testCases" / path


def _shield_yaml_placeholders(text: str) -> tuple[str, dict[str, str]]:
    """把占位符替换成 YAML 安全的临时 token，避免 ``{}`` / ``@`` 被当成语法。"""
    mapping: dict[str, str] = {}

    def _sub(match: re.Match[str]) -> str:
        token = f"{_YAML_SHIELD_PREFIX}{len(mapping)}__"
        mapping[token] = match.group(0)
        return token

    return _YAML_PLACEHOLDER.sub(_sub, text), mapping


def _unshield_yaml_placeholders(value: Any, mapping: dict[str, str]) -> Any:
    """把临时 token 还原成原始占位符字符串。"""
    if not mapping:
        return value
    if isinstance(value, str):
        for token, original in mapping.items():
            if token in value:
                value = value.replace(token, original)
        return value
    if isinstance(value, list):
        return [_unshield_yaml_placeholders(item, mapping) for item in value]
    if isinstance(value, tuple):
        return tuple(_unshield_yaml_placeholders(item, mapping) for item in value)
    if isinstance(value, dict):
        return {
            _unshield_yaml_placeholders(k, mapping): _unshield_yaml_placeholders(v, mapping)
            for k, v in value.items()
        }
    return value


def load_yaml(path: str | Path) -> Any:
    """读取并解析 YAML 测试数据文件。

    支持未加引号的占位符，例如 ``account: {{generate_english_name}}``。
    """
    file_path = _resolve(path)
    with file_path.open("r", encoding="utf-8") as f:
        raw = f.read()
    shielded, mapping = _shield_yaml_placeholders(raw)
    data = yaml.safe_load(shielded)
    return _unshield_yaml_placeholders(data, mapping)


def load_json(path: str | Path) -> Any:
    """读取并解析 JSON 测试数据文件。"""
    file_path = _resolve(path)
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_excel(path: str | Path, sheet_name: str | int = 0) -> list[dict[str, Any]]:
    """读取 Excel 工作表，将首行作为表头并返回字典列表。"""
    from openpyxl import load_workbook

    file_path = _resolve(path)
    wb = load_workbook(file_path, read_only=True, data_only=True)
    if isinstance(sheet_name, str) and sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    elif isinstance(sheet_name, int):
        ws = wb.worksheets[sheet_name]
    else:
        ws = wb.active

    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []
    headers = [str(h) if h is not None else f"col_{i}" for i, h in enumerate(rows[0])]
    result = []
    for row in rows[1:]:
        item = {headers[i]: (row[i] if i < len(row) else None) for i in range(len(headers))}
        result.append(item)
    return result


def parametrize_data(path: str | Path, key: str | None = "cases") -> list[Any]:
    """加载 yaml/json/excel 测试数据；指定 key 时返回对应列表，否则返回整份文档。

    加载后自动解析占位符：
    - ``{{generate_string(12)}}`` / ``{{generate_email}}`` → ``service.utils.random_generator``（无参可省略 ``()``）
    - ``@{api.AITF.create_user()}`` → ``application.datafactory``（无参可省略 ``()``）
    - ``${user}`` → 项目 ``global_var``

    推荐只传文件名（如 ``user.yaml``），自动从调用方同级 ``data/`` 目录加载。
    """
    file_path = _resolve(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    suffix = file_path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        data = load_yaml(file_path)
    elif suffix == ".json":
        data = load_json(file_path)
    elif suffix in {".xlsx", ".xls"}:
        data = load_excel(file_path)
        return _apply_placeholders(data, file_path)
    else:
        raise ValueError(f"Unsupported data file: {file_path}")

    if key is None:
        result = data if isinstance(data, list) else [data]
    elif isinstance(data, dict) and key in data:
        cases = data[key]
        if not isinstance(cases, list):
            raise TypeError(f"data key {key!r} must be a list")
        result = cases
    elif isinstance(data, list):
        result = data
    else:
        raise KeyError(f"Key {key!r} not found in {file_path}")

    return _apply_placeholders(result, file_path)


def _apply_placeholders(data: Any, file_path: Path) -> Any:
    project = resolve_project_from_path(file_path)
    return resolve_placeholders(data, project=project)
