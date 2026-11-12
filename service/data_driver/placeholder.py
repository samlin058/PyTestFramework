"""测试数据占位符解析。

规则：
- ``{{generate_string(12)}}`` / ``{{generate_email}}`` → 调用 ``service.utils.random_generator`` 下同名方法（无参可省略 ``()``）
- ``@{api.AITF.create_user()}`` / ``@{api.AITF.create_user}`` → 调用 ``application.datafactory`` 下对应路径的方法（无参可省略 ``()``）
- ``${user}`` → 读取当前项目 ``global_var``（``service/config/*.yaml``）
"""

from __future__ import annotations

import ast
import importlib
import os
import re
from typing import Any

from service.config import get_project_config, list_projects, resolve_project_name
from service.utils import random_generator as _random_generator

_FULL_RANDOM = re.compile(r"^\{\{(.+)\}\}$", re.DOTALL)
_FULL_FACTORY = re.compile(r"^@\{(.+)\}$", re.DOTALL)
_FULL_GLOBAL = re.compile(r"^\$\{(.+)\}$", re.DOTALL)

_EMBED_RANDOM = re.compile(r"\{\{([^{}]+)\}\}")
_EMBED_FACTORY = re.compile(r"@\{([^}]+)\}")
_EMBED_GLOBAL = re.compile(r"\$\{([^}]+)\}")

_HAS_PLACEHOLDER = re.compile(r"(\{\{[^{}]+\}\}|@\{[^}]+\}|\$\{[^}]+\})")


class PlaceholderError(ValueError):
    """占位符解析失败。"""


def resolve_placeholders(value: Any, *, project: str | None = None) -> Any:
    """递归解析数据结构中的占位符。"""
    global_var = _load_global_var(project)
    return _resolve_any(value, global_var=global_var)


def _load_global_var(project: str | None) -> dict[str, Any]:
    name = (project or "").strip() or (os.getenv("PROJECT") or "").strip()
    if not name:
        projects = list_projects()
        if len(projects) == 1:
            name = projects[0]
        else:
            return {}
    try:
        cfg = get_project_config(name)
    except KeyError:
        return {}
    raw = cfg.get("global_var") or {}
    return dict(raw) if isinstance(raw, dict) else {}


def resolve_project_from_path(path: str | Any) -> str | None:
    """从数据文件路径推断项目名；无法推断时返回 None。"""
    try:
        return resolve_project_name(path)
    except (ValueError, KeyError):
        return None


def _resolve_any(value: Any, *, global_var: dict[str, Any]) -> Any:
    if isinstance(value, str):
        return _resolve_string(value, global_var=global_var)
    if isinstance(value, list):
        return [_resolve_any(item, global_var=global_var) for item in value]
    if isinstance(value, tuple):
        return tuple(_resolve_any(item, global_var=global_var) for item in value)
    if isinstance(value, dict):
        return {k: _resolve_any(v, global_var=global_var) for k, v in value.items()}
    return value


def _resolve_string(text: str, *, global_var: dict[str, Any]) -> Any:
    if not _HAS_PLACEHOLDER.search(text):
        return text

    m = _FULL_RANDOM.fullmatch(text.strip())
    if m:
        return _call_random(m.group(1).strip())

    m = _FULL_FACTORY.fullmatch(text.strip())
    if m:
        return _call_factory(m.group(1).strip())

    m = _FULL_GLOBAL.fullmatch(text.strip())
    if m:
        return _lookup_global(m.group(1).strip(), global_var)

    # 嵌入式占位符：结果一律拼成字符串
    def _sub_random(match: re.Match[str]) -> str:
        return _to_text(_call_random(match.group(1).strip()))

    def _sub_factory(match: re.Match[str]) -> str:
        return _to_text(_call_factory(match.group(1).strip()))

    def _sub_global(match: re.Match[str]) -> str:
        return _to_text(_lookup_global(match.group(1).strip(), global_var))

    result = _EMBED_RANDOM.sub(_sub_random, text)
    result = _EMBED_FACTORY.sub(_sub_factory, result)
    result = _EMBED_GLOBAL.sub(_sub_global, result)
    return result


def _to_text(value: Any) -> str:
    return "" if value is None else str(value)


def _lookup_global(key: str, global_var: dict[str, Any]) -> Any:
    if not key:
        raise PlaceholderError("${} 缺少变量名")
    # 支持 a.b 点路径
    cur: Any = global_var
    for part in key.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise PlaceholderError(f"global_var 中不存在键: {key}")
        cur = cur[part]
    return cur


def _call_random(expr: str) -> Any:
    name, args, kwargs = _parse_call(expr)
    if "." in name:
        raise PlaceholderError(
            f"随机占位符只写方法名即可，例如 {{{{generate_string(12)}}}}，收到: {expr}"
        )
    fn = getattr(_random_generator, name, None)
    if not callable(fn):
        available = ", ".join(_random_generator.__all__)
        raise PlaceholderError(f"未知随机方法: {name}，可选: {available}")
    return fn(*args, **kwargs)


def _call_factory(expr: str) -> Any:
    path, args, kwargs = _parse_call(expr)
    parts = [p for p in path.split(".") if p]
    if len(parts) < 2:
        raise PlaceholderError(
            f"造数占位符格式应为 @{{api.AITF.create_user()}}，收到: {expr}"
        )
    module_name = "application.datafactory." + ".".join(parts[:-1])
    func_name = parts[-1]
    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        raise PlaceholderError(f"无法导入造数模块 {module_name}: {exc}") from exc
    fn = getattr(module, func_name, None)
    if not callable(fn):
        raise PlaceholderError(f"造数模块 {module_name} 中不存在可调用对象: {func_name}")
    return fn(*args, **kwargs)


def _parse_call(expr: str) -> tuple[str, tuple[Any, ...], dict[str, Any]]:
    """解析 ``name(args)`` / ``a.b.c(args)``；无括号时视为无参调用名。"""
    text = expr.strip()
    if not text:
        raise PlaceholderError("占位符表达式为空")

    # 无括号：当作无参函数名 / 路径
    if "(" not in text:
        return text, (), {}

    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError as exc:
        raise PlaceholderError(f"无法解析调用表达式: {expr}") from exc

    node = tree.body
    if not isinstance(node, ast.Call):
        raise PlaceholderError(f"占位符必须是函数调用: {expr}")

    path = _dotted_name(node.func)
    args = tuple(_literal(arg, expr) for arg in node.args)
    kwargs: dict[str, Any] = {}
    for kw in node.keywords:
        if kw.arg is None:
            raise PlaceholderError(f"不支持 *args/**kwargs: {expr}")
        kwargs[kw.arg] = _literal(kw.value, expr)
    return path, args, kwargs


def _dotted_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_dotted_name(node.value)}.{node.attr}"
    raise PlaceholderError(f"不支持的调用目标: {ast.dump(node)}")


def _literal(node: ast.AST, expr: str) -> Any:
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError) as exc:
        raise PlaceholderError(f"参数必须是字面量: {expr}") from exc
