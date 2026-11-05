from __future__ import annotations

import pytest

from core.http import HttpClient


@pytest.fixture(scope="session")
def http_client() -> HttpClient:
    return HttpClient()
