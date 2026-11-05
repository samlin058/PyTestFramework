from __future__ import annotations

import os
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from core.utils.path_util import PROJECT_ROOT

_CONFIG: dict[str, Any] | None = None


def _env_name() -> str:
    """读取当前运行环境名（ENV），默认 test。"""
    return os.getenv("ENV", "test").strip().lower()


def _load_yaml(env: str) -> dict[str, Any]:
    """加载指定环境的 config/<env>.yaml 配置文件。"""
    path = PROJECT_ROOT / "config" / f"{env}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """深度合并字典，override 覆盖 base 中同名键。"""
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def _apply_project_env_overrides(project_cfg: dict[str, Any]) -> None:
    """将命令行/系统环境变量覆盖到单个项目配置。"""
    if os.getenv("API_BASE_URL"):
        project_cfg["api_base_url"] = os.getenv("API_BASE_URL")
    db = project_cfg.setdefault("db", {})
    for key, env_key in (
        ("host", "DB_HOST"),
        ("port", "DB_PORT"),
        ("user", "DB_USER"),
        ("password", "DB_PASSWORD"),
        ("database", "DB_NAME"),
    ):
        if os.getenv(env_key):
            value = os.getenv(env_key)
            db[key] = int(value) if key == "port" else value
    ui = project_cfg.setdefault("ui", {})
    if os.getenv("UI_BASE_URL"):
        ui["base_url"] = os.getenv("UI_BASE_URL")
    if os.getenv("UI_HEADLESS"):
        ui["headless"] = os.getenv("UI_HEADLESS", "true").lower() in {"1", "true", "yes"}


def _apply_env_overrides(cfg: dict[str, Any]) -> dict[str, Any]:
    """用环境变量覆盖 notify，以及指定/全部项目的 api_base_url、db、ui。"""
    notify = cfg.setdefault("notify", {})
    if os.getenv("NOTIFY_WEBHOOK"):
        notify["webhook"] = os.getenv("NOTIFY_WEBHOOK")

    projects = cfg.setdefault("projects", {})
    target = (os.getenv("PROJECT") or "").strip()
    names = [target] if target and target in projects else list(projects.keys())
    for name in names:
        project_cfg = projects.setdefault(name, {})
        _apply_project_env_overrides(project_cfg)
    return cfg


@lru_cache(maxsize=1)
def get_config() -> dict[str, Any]:
    """获取当前环境的完整配置（含 projects），首次调用时加载并应用环境变量覆盖。"""
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = _apply_env_overrides(_load_yaml(_env_name()))
    return _CONFIG


def list_projects() -> list[str]:
    """返回当前环境配置中的项目名列表。"""
    return list((get_config().get("projects") or {}).keys())


def get_project_config(project: str) -> dict[str, Any]:
    """按项目名加载配置：defaults 与 projects.<name> 深度合并。"""
    cfg = get_config()
    projects = cfg.get("projects") or {}
    if project not in projects:
        available = ", ".join(projects) or "(none)"
        raise KeyError(f"Project {project!r} not found in config. Available: {available}")
    merged = _deep_merge(cfg.get("defaults") or {}, projects[project] or {})
    merged["project"] = project
    merged["env"] = cfg.get("env")
    if "notify" not in merged and cfg.get("notify") is not None:
        merged["notify"] = deepcopy(cfg["notify"])
    return merged


def resolve_project_name(path: str | Path) -> str:
    """从用例路径解析项目名，约定 testCases/<api|ui>/<project>/..."""
    parts = Path(path).resolve().parts
    try:
        idx = parts.index("testCases")
    except ValueError as exc:
        raise ValueError(f"Path is not under testCases: {path}") from exc
    if len(parts) <= idx + 2:
        raise ValueError(
            f"Cannot resolve project from path {path}; expected testCases/<api|ui>/<project>/..."
        )
    layer = parts[idx + 1]
    if layer not in {"api", "ui"}:
        raise ValueError(f"Unexpected test layer {layer!r} in path {path}")
    return parts[idx + 2]


def reload_config() -> dict[str, Any]:
    """清除配置缓存并重新加载，返回最新配置。"""
    global _CONFIG
    get_config.cache_clear()
    _CONFIG = None
    return get_config()
