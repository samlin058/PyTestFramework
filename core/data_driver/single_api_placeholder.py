from __future__ import annotations

import importlib
import inspect
import re
from typing import Any

_AT_FULL = re.compile(r"^@\{([^}]+)\}$")
_AT_EMBEDDED = re.compile(r"@\{([^}]+)\}")
_DOLLAR_FULL = re.compile(r"^\$\{([^}]+)\}$")
_DOLLAR_EMBEDDED = re.compile(r"\$\{([^}]+)\}")
_HASH_FULL = re.compile(r"^#\{([^}]+)\}$")
_HASH_EMBEDDED = re.compile(r"#\{([^}]+)\}")
_MUSTACHE = re.compile(r"\{\{([^{}]+)\}\}")

_RANDOM_GENERATOR_ROOT = "core.utils.random_generator"


class PlaceholderError(ValueError):
    """占位符解析失败。"""


def resolve_placeholders(
    value: Any,
    *,
    global_var: dict[str, Any] | None = None,
    factory_context: dict[str, Any] | None = None,
) -> Any:
    """递归解析 @{}（数据工厂）、${}（随机生成器）与 #{}（global_var）。"""
    gvars = global_var or {}
    ctx = factory_context or {}
    if isinstance(value, dict):
        return {
            k: resolve_placeholders(v, global_var=gvars, factory_context=ctx)
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [
            resolve_placeholders(v, global_var=gvars, factory_context=ctx) for v in value
        ]
    if isinstance(value, str):
        return _resolve_string(value, global_var=gvars, factory_context=ctx)
    return value


def render_mustache(template: str, variables: dict[str, Any]) -> str:
    """将 SQL 等模板中的 {{var}} 替换为 extract 变量值。"""

    def repl(match: re.Match[str]) -> str:
        key = match.group(1).strip()
        if key not in variables:
            raise PlaceholderError(
                f"Unknown extract variable {{{{{key}}}}}；available={list(variables)}"
            )
        return str(variables[key])

    return _MUSTACHE.sub(repl, template)


def _resolve_string(
    text: str,
    *,
    global_var: dict[str, Any],
    factory_context: dict[str, Any],
) -> Any:
    at_full = _AT_FULL.match(text.strip())
    if at_full:
        return _call_factory(at_full.group(1).strip(), factory_context)

    dollar_full = _DOLLAR_FULL.match(text.strip())
    if dollar_full:
        return _call_random_generator(dollar_full.group(1).strip())

    hash_full = _HASH_FULL.match(text.strip())
    if hash_full:
        return _lookup_global(hash_full.group(1).strip(), global_var)

    def at_repl(match: re.Match[str]) -> str:
        return str(_call_factory(match.group(1).strip(), factory_context))

    def dollar_repl(match: re.Match[str]) -> str:
        return str(_call_random_generator(match.group(1).strip()))

    def hash_repl(match: re.Match[str]) -> str:
        return str(_lookup_global(match.group(1).strip(), global_var))

    result = _AT_EMBEDDED.sub(at_repl, text)
    result = _DOLLAR_EMBEDDED.sub(dollar_repl, result)
    result = _HASH_EMBEDDED.sub(hash_repl, result)
    return result


def _lookup_global(path: str, global_var: dict[str, Any]) -> Any:
    if not path:
        raise PlaceholderError("Empty #{} placeholder")
    cur: Any = global_var
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise PlaceholderError(
                f"global_var path #{{{path}}} not found (missing {part!r})"
            )
        cur = cur[part]
    return cur


def _call_random_generator(path: str) -> Any:
    """解析 ${module.func}，调用 core.utils.random_generator 下的方法。"""
    if not path:
        raise PlaceholderError("Empty ${} placeholder")

    parts = path.split(".")
    if len(parts) < 2:
        raise PlaceholderError(
            f"Invalid random placeholder ${{{path}}}: "
            "expected 'module.function' under core.utils.random_generator "
            "(e.g. name_generator.generate_chinese_name)"
        )

    module_name, *attr_parts = parts
    full_mod = f"{_RANDOM_GENERATOR_ROOT}.{module_name}"
    try:
        module = importlib.import_module(full_mod)
    except ImportError as exc:
        raise PlaceholderError(
            f"Cannot import random generator ${{{path}}}: {exc}"
        ) from exc

    target: Any = module
    for name in attr_parts:
        if not hasattr(target, name):
            raise PlaceholderError(
                f"Cannot resolve ${{{path}}}: attribute {name!r} not found on {target!r}"
            )
        target = getattr(target, name)

    if callable(target):
        return target()
    return target


def _call_factory(path: str, factory_context: dict[str, Any]) -> Any:
    if not path:
        raise PlaceholderError("Empty @{} placeholder")
    if not (path.startswith("api.") or path.startswith("db.")):
        raise PlaceholderError(
            f"Invalid factory placeholder @{{{path}}}: "
            "only 'api.' or 'db.' prefixes are allowed"
        )

    full_path = f"datafactory.{path}"
    parts = full_path.split(".")
    module = None
    remaining: list[str] = []
    last_error: Exception | None = None
    for i in range(len(parts), 0, -1):
        mod_name = ".".join(parts[:i])
        try:
            module = importlib.import_module(mod_name)
            remaining = parts[i:]
            break
        except ImportError as exc:
            last_error = exc
            continue
    if module is None:
        raise PlaceholderError(
            f"Cannot import factory path @{{{path}}}: {last_error}"
        ) from last_error

    if not remaining:
        raise PlaceholderError(
            f"Factory path @{{{path}}} points to a module, expected a callable"
        )

    target: Any = module
    for idx, name in enumerate(remaining):
        if inspect.isclass(target):
            target = _instantiate(target, factory_context)
        if hasattr(target, name):
            target = getattr(target, name)
            continue
        # 模块上找不到属性时，尝试模块内 Factory 类上的方法
        if target is module and idx == 0:
            factory_cls = _find_factory_class(module, name)
            if factory_cls is not None:
                instance = _instantiate(factory_cls, factory_context)
                if hasattr(instance, name):
                    target = getattr(instance, name)
                    continue
        raise PlaceholderError(
            f"Cannot resolve @{{{path}}}: attribute {name!r} not found on {target!r}"
        )

    if inspect.isclass(target):
        target = _instantiate(target, factory_context)
    if callable(target):
        return target()
    return target


def _find_factory_class(module: Any, method_name: str) -> type | None:
    candidates: list[type] = []
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ != module.__name__:
            continue
        if hasattr(obj, method_name) and callable(getattr(obj, method_name)):
            candidates.append(obj)
    if not candidates:
        return None
    preferred = [c for c in candidates if c.__name__.endswith("Factory")]
    return (preferred or candidates)[0]


def _instantiate(cls: type, factory_context: dict[str, Any]) -> Any:
    try:
        sig = inspect.signature(cls.__init__)
    except (TypeError, ValueError):
        return cls()

    kwargs: dict[str, Any] = {}
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        if name in factory_context:
            kwargs[name] = factory_context[name]
        elif param.default is not inspect.Parameter.empty:
            continue
        elif param.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            continue
        else:
            raise PlaceholderError(
                f"Cannot instantiate {cls.__name__}: missing required arg {name!r}; "
                f"available context keys={list(factory_context)}"
            )
    return cls(**kwargs)


def bind_factory_context(
    *,
    http_client: Any = None,
    db: Any = None,
    **extra: Any,
) -> dict[str, Any]:
    """构建工厂实例化上下文。"""
    ctx: dict[str, Any] = dict(extra)
    if http_client is not None:
        ctx["http_client"] = http_client
    if db is not None:
        ctx["db"] = db
    return ctx
