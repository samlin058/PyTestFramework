from __future__ import annotations

from pathlib import Path

import allure
import pytest

_API_ROOT = Path(__file__).resolve().parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """自动为 testCases/api 下用例打上 api 标记，无需每个方法再写 @pytest.mark.api。"""
    for item in items:
        try:
            Path(item.path).resolve().relative_to(_API_ROOT)
        except ValueError:
            continue
        item.add_marker(pytest.mark.api)


@pytest.fixture(autouse=True)
def _allure_api_feature() -> None:
    """自动为 testCases/api 下用例打上 Allure Feature=API。"""
    allure.dynamic.feature("API")
