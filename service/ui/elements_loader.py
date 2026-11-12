from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from service.utils.path_util import PROJECT_ROOT


def elements_path(project: str, page_name: str) -> Path:
    """返回 `domain/assets/ui/<project>/<page_name>.yaml` 路径。"""
    return PROJECT_ROOT / "domain" / "assets" / "ui" / project / f"{page_name}.yaml"


def load_ui_elements(project: str, page_name: str) -> dict[str, str]:
    """加载页面元素定位表。

    YAML 支持两种形态：
    - 扁平：`username: "#username"`
    - 嵌套：`elements: { username: "#username" }`
    """
    path = elements_path(project, page_name)
    if not path.is_file():
        raise FileNotFoundError(f"UI elements file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data: Any = yaml.safe_load(f) or {}

    raw = data.get("elements") if isinstance(data, dict) and "elements" in data else data
    if not isinstance(raw, dict) or not raw:
        raise ValueError(f"No element locators in {path}")

    locators: dict[str, str] = {}
    for name, selector in raw.items():
        if selector is None or str(selector).strip() == "":
            raise ValueError(f"Empty selector for element {name!r} in {path}")
        locators[str(name)] = str(selector)
    return locators
