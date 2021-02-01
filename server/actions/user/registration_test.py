import pytest

from actions.user.registration import (
    UserRegistration,
    EmailAlreadyRegisteredException,
    UsernameAlreadyRegisteredException,
)
from data_models.users import UserCreate
from database_schemas.users import UserEntry


class TestCreateUser(object):
    def test_new_user(
        self, user_registration: UserRegistration, user_create_squirtle: UserCreate
    ):
        new_user = user_registration.create_user(user_create_squirtle)
        assert isinstance(new_user.id, int)

    def test_existing_username_user(
        self,
        user_registration: UserRegistration,
        user_entry_squirtle: UserEntry,
    ):
        with pytest.raises(UsernameAlreadyRegisteredException):
            new_email = "new_squirtle@example.com"
            new_user = UserCreate(
                **{
                    "username": user_entry_squirtle.username,
                    "email": new_email,
                    "password": "password",
                }
            )
            user_registration.create_user(new_user)

    def test_existing_email_user(
        self,
        user_registration: UserRegistration,
        user_entry_squirtle: UserEntry,
    ):
        with pytest.raises(EmailAlreadyRegisteredException):
            new_username = "new_squirtle"
            new_user = UserCreate(
                **{
                    "username": new_username,
                    "email": user_entry_squirtle.email,
                    "password": "password",
                }
            )
            user_registration.create_user(new_user)
