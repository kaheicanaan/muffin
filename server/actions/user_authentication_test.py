from datetime import datetime, timedelta
import pytest

from actions.user_authentication import UserAuthentication, InvalidCredentialsException
from database_schemas.users import UserEntry
from data_models.access_token import UserToken


@pytest.fixture(name="user_authentication")
def fixture_user_authentication(user_profile):
    return UserAuthentication(user_profile)


class TestLoginUser(object):
    def test_valid_login(
        self, user_authentication: UserAuthentication, user_entry_squirtle: UserEntry
    ):
        user_token = user_authentication.login(user_entry_squirtle.email, "password")
        assert isinstance(user_token, UserToken)
        assert user_token.user_id == user_entry_squirtle.id

    def test_wrong_password(
        self, user_authentication: UserAuthentication, user_entry_squirtle: UserEntry
    ):
        with pytest.raises(InvalidCredentialsException):
            user_authentication.login(user_entry_squirtle.email, "wrongpassword")

    def test_unknown_user(self, user_authentication: UserAuthentication):
        with pytest.raises(InvalidCredentialsException):
            user_authentication.login("pusheen@example.com", "password")


class TestSignToken(object):
    def test_sign_token(self, user_authentication: UserAuthentication):
        signed_token = user_authentication.sign_token(
            {"user_id": 1, "exp": datetime.utcnow()}
        )
        assert isinstance(signed_token, str)


class TestGetAuthorizedUser(object):
    def test_valid_token(
        self, user_authentication: UserAuthentication, user_entry_squirtle: UserEntry
    ):
        user_token = user_authentication.sign_token(
            user_authentication.login(user_entry_squirtle.email, "password").dict()
        )
        authorized_user_entry = user_authentication.get_authorized_user(user_token)
        assert isinstance(authorized_user_entry, UserEntry)
        assert authorized_user_entry.id == user_entry_squirtle.id

    def test_invalid_token(self, user_authentication: UserAuthentication):
        user_token = "invalid_token"
        with pytest.raises(InvalidCredentialsException):
            user_authentication.get_authorized_user(user_token)

    def test_expired_token(
        self, user_authentication: UserAuthentication, user_entry_squirtle: UserEntry
    ):
        user_token = user_authentication.sign_token(
            UserToken(
                user_id=user_entry_squirtle.id,
                exp=datetime.utcnow() - timedelta(minutes=10),
            ).dict()
        )
        with pytest.raises(InvalidCredentialsException):
            user_authentication.get_authorized_user(user_token)
