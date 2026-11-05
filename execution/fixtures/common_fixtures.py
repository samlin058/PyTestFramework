from __future__ import annotations

import pytest

from core.config import get_config
from core.database import DatabaseClient
from datafactory.api.AITF.user_factory import UserDataFactory


@pytest.fixture(scope="session")
def env_config():
    return get_config()


@pytest.fixture(scope="session")
def db(env_config):
    client = DatabaseClient(env_config.get("db"))
    if client.enabled:
        client.connect()
    yield client
    client.close()


@pytest.fixture
def user_factory(http_client, db) -> UserDataFactory:
    return UserDataFactory(http_client=http_client, db=db)
