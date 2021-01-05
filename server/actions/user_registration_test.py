import pytest

from actions.user_profile import UserProfile
from actions.user_registration import UserRegistration, UserAlreadyExistsException
from data_models.users import UserCreate
from database_schemas.base import Base
from database_schemas.db_session import sqlite_db_session, test_engine


@pytest.fixture(name="db")
def fixture_db():
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    return next(sqlite_db_session())


@pytest.fixture(name="user_registration")
def fixture_user_registration(db) -> UserRegistration:
    return UserRegistration(db, UserProfile(db))


@pytest.fixture(name="user_create")
def fixture_user_create() -> UserCreate:
    return UserCreate(**{"email": "user@example.com", "password": "password"})


class TestCreateUser(object):
    def test_new_user(
        self, user_registration: UserRegistration, user_create: UserCreate
    ):
        new_user = user_registration.create_user(user_create)
        assert isinstance(new_user.id, int)

    def test_existing_user(
        self, user_registration: UserRegistration, user_create: UserCreate
    ):
        new_user = user_registration.create_user(user_create)
        assert isinstance(new_user.id, int)
        with pytest.raises(UserAlreadyExistsException):
            user_registration.create_user(user_create)
