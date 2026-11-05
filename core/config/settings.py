from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import yaml
from dotenv import load_dotenv

from core.utils.path_util import PROJECT_ROOT

load_dotenv(PROJECT_ROOT / ".env")

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


def _apply_env_overrides(cfg: dict[str, Any]) -> dict[str, Any]:
    """用环境变量覆盖配置中的 base_url、数据库、通知与 UI 相关项。"""
    if os.getenv("BASE_URL"):
        cfg["base_url"] = os.getenv("BASE_URL")
    db = cfg.setdefault("db", {})
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
    notify = cfg.setdefault("notify", {})
    if os.getenv("NOTIFY_WEBHOOK"):
        notify["webhook"] = os.getenv("NOTIFY_WEBHOOK")
    ui = cfg.setdefault("ui", {})
    if os.getenv("UI_BASE_URL"):
        ui["base_url"] = os.getenv("UI_BASE_URL")
    if os.getenv("UI_HEADLESS"):
        ui["headless"] = os.getenv("UI_HEADLESS", "true").lower() in {"1", "true", "yes"}
    return cfg


@lru_cache(maxsize=1)
def get_config() -> dict[str, Any]:
    """获取当前环境的全局配置（带缓存），首次调用时加载并应用环境变量覆盖。"""
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = _apply_env_overrides(_load_yaml(_env_name()))
    return _CONFIG


def reload_config() -> dict[str, Any]:
    """清除配置缓存并重新加载，返回最新配置。"""
    global _CONFIG
    get_config.cache_clear()
    _CONFIG = None
    return get_config()
