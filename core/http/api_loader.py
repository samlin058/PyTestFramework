from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from core.logger import logger
from core.utils.path_util import PROJECT_ROOT


def extract_body_defaults(body: Any) -> dict[str, Any]:
    """从 assets body 提取默认请求体。

    - schema 形态（含 properties.*.default）→ 扁平 defaults
    - 普通 dict → 原样作为 defaults
    """
    if not isinstance(body, dict) or not body:
        return {}
    props = body.get("properties")
    if isinstance(props, dict):
        defaults: dict[str, Any] = {}
        for key, schema in props.items():
            if isinstance(schema, dict) and "default" in schema:
                defaults[key] = schema["default"]
        return defaults
    return dict(body)


class ApiSpecLoader:
    """Load controller YAML specs; index by (controller, url) and (controller, name)."""

    def __init__(self, specs_dir: str | Path | None = None) -> None:
        """初始化 API 规格加载器，指定或默认使用 assets/api 目录。"""
        # assets/api/<project>/*.yaml，按项目分子目录管理
        self.specs_dir = Path(specs_dir) if specs_dir else PROJECT_ROOT / "assets" / "api"
        self._by_controller_url: dict[tuple[str, str], dict[str, Any]] = {}
        self._by_controller_name: dict[tuple[str, str], dict[str, Any]] = {}
        self._loaded = False

    def load(self) -> None:
        """扫描并加载所有 YAML 接口规格，按 url / name 建立索引。"""
        self._by_controller_url.clear()
        self._by_controller_name.clear()
        if not self.specs_dir.exists():
            raise FileNotFoundError(f"API specs directory not found: {self.specs_dir}")
        yaml_files = sorted(self.specs_dir.glob("*/*.yaml"))
        if not yaml_files:
            raise FileNotFoundError(
                f"No API specs found under {self.specs_dir}/<project>/*.yaml"
            )
        for path in yaml_files:
            with path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            controller = data.get("controller") or path.stem
            project = path.parent.name
            for api in data.get("apis") or []:
                url = api.get("url")
                if not url:
                    raise ValueError(f"Missing url in {path.name}: {api}")
                name = api.get("name") or url
                body = api.get("body")
                spec = {
                    "controller": controller,
                    "project": project,
                    "name": name,
                    "method": str(api.get("method", "GET")).upper(),
                    "url": url,
                    "headers": api.get("headers") or {},
                    "params": api.get("params") or {},
                    "body": body,
                    "body_defaults": extract_body_defaults(body),
                    "timeout": api.get("timeout"),
                    "source": str(path),
                }
                url_key = (controller, url)
                name_key = (controller, name)
                if name_key in self._by_controller_name:
                    raise ValueError(
                        f"Duplicate API name {name!r} under controller={controller!r} "
                        f"in {path}"
                    )
                self._by_controller_url[url_key] = spec
                self._by_controller_name[name_key] = spec
            logger.debug(
                f"Loaded API spec: {project}/{path.name} controller={controller}"
            )
        self._loaded = True

    def ensure_loaded(self) -> None:
        """确保规格已加载；若尚未加载则触发一次 load。"""
        if not self._loaded:
            self.load()

    def get(self, controller: str, url: str) -> dict[str, Any]:
        """根据 controller 与 url 获取对应接口规格，找不到则抛出 KeyError。"""
        self.ensure_loaded()
        key = (controller, url)
        if key not in self._by_controller_url:
            raise KeyError(f"API not found for controller={controller!r}, url={url!r}")
        return self._by_controller_url[key]

    def get_by_name(self, controller: str, name: str) -> dict[str, Any]:
        """根据 controller 与接口 name 获取规格，找不到则抛出 KeyError。"""
        self.ensure_loaded()
        key = (controller, name)
        if key not in self._by_controller_name:
            raise KeyError(f"API not found for controller={controller!r}, name={name!r}")
        return self._by_controller_name[key]

    def all_specs(self) -> list[dict[str, Any]]:
        """返回已加载的全部接口规格列表。"""
        self.ensure_loaded()
        return list(self._by_controller_url.values())
