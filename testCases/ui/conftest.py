from __future__ import annotations

from pathlib import Path

import allure
import pytest

_UI_ROOT = Path(__file__).resolve().parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """自动为 testCases/ui 下用例打上 ui 标记，无需每个方法再写 @pytest.mark.ui。"""
    for item in items:
        try:
            Path(item.path).resolve().relative_to(_UI_ROOT)
        except ValueError:
            continue
        item.add_marker(pytest.mark.ui)


@pytest.fixture(autouse=True)
def _allure_ui_feature() -> None:
    """自动为 testCases/ui 下用例打上 Allure Feature=UI。"""
    allure.dynamic.feature("UI")
