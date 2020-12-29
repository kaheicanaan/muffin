import pytest

from database_schemas.base import db_session


@pytest.fixture
def db():
    return db_session()


@pytest.fixture
def sample_user() -> dict:
    return {"email": "user@example.com", "password": "password"}
