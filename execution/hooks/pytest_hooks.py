from __future__ import annotations

import allure
import pytest


def pytest_configure(config):  # noqa: ARG001
    """Hook placeholder; markers are declared in pytest.ini."""


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):  # noqa: ARG001
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            try:
                png = page.screenshot(type="png", full_page=True)
                allure.attach(png, name="failure_screenshot", attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass
