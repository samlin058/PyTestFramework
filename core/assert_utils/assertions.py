from __future__ import annotations

from typing import Any

import allure
from jsonpath_ng import parse

from core.logger import logger


class AssertUtils:
    @staticmethod
    def equal(actual: Any, expected: Any, msg: str = "") -> None:
        """断言实际值与期望值相等，并写入 Allure 步骤。"""
        with allure.step(f"assert equal: {msg or f'{actual!r} == {expected!r}'}"):
            assert actual == expected, msg or f"expected {expected!r}, got {actual!r}"

    @staticmethod
    def status_code(response: Any, expected: int) -> None:
        """断言 HTTP 响应状态码等于期望值。"""
        actual = getattr(response, "status_code", None)
        with allure.step(f"assert status_code == {expected}"):
            assert actual == expected, f"status_code expected {expected}, got {actual}"

    @staticmethod
    def contains(text: Any, part: Any, msg: str = "") -> None:
        """断言文本或容器中包含指定片段。"""
        with allure.step(f"assert contains: {part!r} in {text!r}"):
            assert part in text, msg or f"{part!r} not in {text!r}"

    @staticmethod
    def json_path_equals(payload: Any, expr: str, expected: Any) -> None:
        """用 JSONPath 提取字段并断言其值等于期望值。"""
        matches = [m.value for m in parse(expr).find(payload)]
        with allure.step(f"assert jsonpath {expr} == {expected!r}"):
            assert matches, f"jsonpath {expr} matched nothing"
            assert matches[0] == expected, f"jsonpath {expr}: expected {expected!r}, got {matches[0]!r}"

    @staticmethod
    def true(condition: bool, msg: str = "") -> None:
        """断言条件为真，失败时抛出带消息的 AssertionError。"""
        with allure.step(f"assert true: {msg or condition}"):
            assert condition, msg or "condition is False"
        logger.debug(f"assert passed: {msg}")
