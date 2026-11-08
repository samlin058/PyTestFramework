from __future__ import annotations

from typing import Any

import allure
from jsonpath_ng import parse

from core.assert_utils import AssertUtils
from core.data_driver.single_api_placeholder import render_mustache
from core.database import DatabaseClient
from core.logger import logger


def extract_vars(payload: Any, extract: dict[str, Any] | None) -> dict[str, Any]:
    """按 case.extract 从响应 JSON 提取变量；失败则抛错。"""
    if not extract:
        return {}
    if not isinstance(extract, dict):
        raise ValueError(f"extract must be a mapping, got {type(extract).__name__}")

    variables: dict[str, Any] = {}
    with allure.step(f"extract vars: {list(extract)}"):
        for name, expr in extract.items():
            if not isinstance(expr, str) or not expr.strip():
                raise ValueError(f"extract[{name!r}] must be a non-empty JSONPath string")
            matches = [m.value for m in parse(expr).find(payload)]
            if not matches:
                raise AssertionError(f"extract {name!r}: jsonpath {expr} matched nothing")
            variables[name] = matches[0]
            logger.info(f"extract {name}={variables[name]!r} from {expr}")
    return variables


def run_assertions(
    *,
    response: Any,
    assertions: list[dict[str, Any]] | None,
    db: DatabaseClient | None = None,
    variables: dict[str, Any] | None = None,
) -> None:
    """执行 YAML assertions 列表。"""
    if not assertions:
        return
    vars_map = variables or {}
    try:
        payload = response.json()
    except Exception:
        payload = None

    for index, assertion in enumerate(assertions):
        if not isinstance(assertion, dict):
            raise ValueError(f"assertions[{index}] must be a mapping")
        assert_type = assertion.get("type")
        with allure.step(f"assertion[{index}] type={assert_type}"):
            if assert_type == "status_code":
                expected = assertion.get("expected")
                if expected is None:
                    raise ValueError(f"assertions[{index}] status_code missing expected")
                AssertUtils.status_code(response, int(expected))
            elif assert_type == "json_path":
                _assert_json_path(payload, assertion, index)
            elif assert_type == "db":
                _assert_db(assertion, index, db=db, variables=vars_map)
            else:
                raise ValueError(
                    f"assertions[{index}] unsupported type {assert_type!r}; "
                    "expected status_code | json_path | db"
                )


def _assert_json_path(payload: Any, assertion: dict[str, Any], index: int) -> None:
    if payload is None:
        raise AssertionError(f"assertions[{index}] json_path: response is not JSON")
    path = assertion.get("path")
    if not path:
        raise ValueError(f"assertions[{index}] json_path missing path")
    operator = (assertion.get("operator") or "eq").lower()
    if operator == "exists":
        AssertUtils.json_path_exists(payload, path)
        return
    if "expected" not in assertion:
        raise ValueError(
            f"assertions[{index}] json_path missing expected "
            f"(or use operator: exists)"
        )
    AssertUtils.json_path_equals(payload, path, assertion.get("expected"))


def _assert_db(
    assertion: dict[str, Any],
    index: int,
    *,
    db: DatabaseClient | None,
    variables: dict[str, Any],
) -> None:
    if db is None:
        raise RuntimeError(f"assertions[{index}] db: DatabaseClient is not available")
    if not db.enabled:
        raise RuntimeError(
            f"assertions[{index}] db: database is disabled; "
            "set projects.<project>.db.enabled=true"
        )
    sql = assertion.get("sql")
    if not sql or not isinstance(sql, str):
        raise ValueError(f"assertions[{index}] db missing sql")
    if "expected" not in assertion:
        raise ValueError(f"assertions[{index}] db missing expected")

    rendered_sql = render_mustache(sql, variables)
    row = db.fetch_one(rendered_sql)
    with allure.step(f"assert db: {rendered_sql}"):
        assert row is not None, f"db assertion returned no row for sql={rendered_sql!r}"
        column = assertion.get("column")
        if column:
            if column not in row:
                raise AssertionError(
                    f"db assertion column {column!r} not in row keys={list(row)}"
                )
            actual = row[column]
        else:
            actual = next(iter(row.values()))
        expected = assertion.get("expected")
        assert actual == expected, (
            f"db assertion expected {expected!r}, got {actual!r}; row={row}"
        )
