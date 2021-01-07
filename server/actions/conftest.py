import pytest

from actions.user_profile import UserProfile
from actions.user_registration import UserRegistration
from data_models.users import UserCreate
from database_schemas.base import Base
from database_schemas.db_session import sqlite_db_session, test_engine


# DB Session
@pytest.fixture(name="db")
def fixture_db():
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    return next(sqlite_db_session())


# Actions
@pytest.fixture(name="user_profile")
def fixture_user_profile(db) -> UserProfile:
    return UserProfile(db)


@pytest.fixture(name="user_registration")
def fixture_user_registration(db, user_profile) -> UserRegistration:
    return UserRegistration(db, user_profile)


# Dummy Users
@pytest.fixture(name="user_squirtle")
def fixture_user_squirtle() -> UserCreate:
    return UserCreate(**{"email": "squirtle@example.com", "password": "password"})


@pytest.fixture(name="user_zenigame")
def fixture_user_zenigame() -> UserCreate:
    return UserCreate(**{"email": "zenigame@example.com", "password": "Password"})
