import pytest

from actions.user_profile import UserProfile
from actions.user_registration import UserRegistration
from data_models.users import UserCreate
from database_schemas.base import Base
from database_schemas.db_session import sqlite_db_session, test_engine


@pytest.fixture(name="db")
def fixture_db():
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    return next(sqlite_db_session())


@pytest.fixture(name="user_registration_action")
def fixture_user_registration_action(db) -> UserRegistration:
    return UserRegistration(db, UserProfile(db))


@pytest.fixture(name="sample_user")
def fixture_sample_user() -> dict:
    return {"email": "user@example.com", "password": "password"}


def test_create_user(user_registration_action, sample_user):
    sample_user_model = UserCreate(**sample_user)
    db_user = user_registration_action.create_user(sample_user_model)
    assert isinstance(db_user.id, int)


def test_create_user_2(user_registration_action, sample_user):
    # ensure the previous created user is destroyed for every function
    sample_user_model = UserCreate(**sample_user)
    db_user = user_registration_action.create_user(sample_user_model)
    assert isinstance(db_user.id, int)
