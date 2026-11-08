from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from core.config import resolve_project_name
from core.http.api_loader import ApiSpecLoader
from core.utils.path_util import PROJECT_ROOT


def is_single_api_yaml(path: Path) -> bool:
    """判断路径是否为 testCases/api/<project>/single/*.yaml。"""
    parts = path.resolve().parts
    try:
        idx = parts.index("testCases")
    except ValueError:
        return False
    if len(parts) < idx + 5:
        return False
    return (
        parts[idx + 1] == "api"
        and parts[idx + 3] == "single"
        and path.suffix.lower() in {".yaml", ".yml"}
    )


def load_single_api_file(
    path: str | Path,
    api_loader: ApiSpecLoader | None = None,
) -> list[dict[str, Any]]:
    """加载一份单接口 YAML，展开为可执行 case 单元列表。"""
    file_path = Path(path).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"Single API case file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Single API YAML must be a mapping: {file_path}")

    controller = data.get("controller")
    api_name = data.get("api_name")
    cases = data.get("cases")
    if not controller:
        raise ValueError(f"Missing controller in {file_path}")
    if not api_name:
        raise ValueError(f"Missing api_name in {file_path}")
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"cases must be a non-empty list in {file_path}")

    project = resolve_project_name(file_path)
    loader = api_loader or ApiSpecLoader()
    spec = loader.get_by_name(controller, api_name)

    module = data.get("module") or ""
    api_desc = data.get("api_desc") or ""
    units: list[dict[str, Any]] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise ValueError(f"case[{index}] must be a mapping in {file_path}")
        merged = merge_case_with_spec(case, spec)
        units.append(
            {
                "project": project,
                "module": module,
                "api_desc": api_desc,
                "controller": controller,
                "api_name": api_name,
                "case": case,
                "request": merged,
                "yaml_path": str(file_path),
                "case_index": index,
            }
        )
    return units


def merge_case_with_spec(case: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    """合并 case 与 assets 默认值；空则回落，都空则不传。"""
    spec_headers = dict(spec.get("headers") or {})
    case_headers = case.get("headers")
    if _is_empty_mapping(case_headers):
        headers = spec_headers or None
    else:
        headers = {**spec_headers, **dict(case_headers)} or None

    spec_params = dict(spec.get("params") or {})
    case_params = case.get("params")
    if _is_empty_mapping(case_params):
        params = spec_params or None
    else:
        params = {**spec_params, **dict(case_params)} or None

    case_path_params = case.get("path_params")
    path_params = None if _is_empty_mapping(case_path_params) else dict(case_path_params)

    case_body = case.get("body")
    if _is_empty_mapping(case_body):
        body_defaults = dict(spec.get("body_defaults") or {})
        body = body_defaults or None
    elif isinstance(case_body, dict):
        body = dict(case_body)
    else:
        # 允许整段 body 为 @{...} / ${...} 等占位符，解析阶段再展开
        body = case_body

    return {
        "headers": headers,
        "params": params,
        "path_params": path_params,
        "body": body,
    }


def _is_empty_mapping(value: Any) -> bool:
    return value is None or (isinstance(value, dict) and len(value) == 0)


def discover_single_api_yaml_files(
    root: str | Path | None = None,
) -> list[Path]:
    """扫描 testCases/api/**/single/*.yaml。"""
    base = Path(root) if root else PROJECT_ROOT / "testCases" / "api"
    if not base.exists():
        return []
    files = sorted(base.glob("*/single/*.yaml")) + sorted(base.glob("*/single/*.yml"))
    return [p.resolve() for p in files]
