from __future__ import annotations

import inspect
import json
from pathlib import Path
from typing import Any

import yaml

from core.utils.path_util import PROJECT_ROOT, resolve_path


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
    - 仅文件名（如 login_cases.yaml）：优先取调用方同级 data/<文件名>
    - 其它相对路径：项目根 → testCases/<path>
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
    return PROJECT_ROOT / "testCases" / path


def load_yaml(path: str | Path) -> Any:
    """读取并解析 YAML 测试数据文件。"""
    file_path = _resolve(path)
    with file_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


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

    推荐只传文件名（如 ``login_cases.yaml``），自动从调用方同级 ``data/`` 目录加载。
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
        return load_excel(file_path)
    else:
        raise ValueError(f"Unsupported data file: {file_path}")

    if key is None:
        return data if isinstance(data, list) else [data]
    if isinstance(data, dict) and key in data:
        cases = data[key]
        if not isinstance(cases, list):
            raise TypeError(f"data key {key!r} must be a list")
        return cases
    if isinstance(data, list):
        return data
    raise KeyError(f"Key {key!r} not found in {file_path}")
