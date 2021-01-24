import pytest

from actions.user.registration import (
    UserRegistration,
    UserAlreadyExistsException,
)
from data_models.users import UserCreate


class TestCreateUser(object):
    def test_new_user(
        self, user_registration: UserRegistration, user_create_squirtle: UserCreate
    ):
        new_user = user_registration.create_user(user_create_squirtle)
        assert isinstance(new_user.id, int)

    def test_existing_user(
        self, user_registration: UserRegistration, user_create_squirtle: UserCreate
    ):
        new_user = user_registration.create_user(user_create_squirtle)
        assert isinstance(new_user.id, int)
        with pytest.raises(UserAlreadyExistsException):
            user_registration.create_user(user_create_squirtle)
