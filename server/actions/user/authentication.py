import os
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import EmailStr

from actions import utils
from actions.user.profile import UserProfile, UserNotFoundException
from data_models.access_token import UserToken
from database_schemas.users import UserEntry

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="login")

_ACCESS_TOKEN_ALGORITHM = jwt.ALGORITHMS.HS256
_ACCESS_TOKEN_EXPIRATION = timedelta(minutes=30)


class InvalidCredentialsException(Exception):
    pass


class UserAuthentication(object):
    def __init__(self, user_profile: UserProfile = Depends()):
        self.user_profile = user_profile

    def login(self, email: EmailStr, password: str) -> UserToken:
        try:
            user_entry = self.user_profile.get_by_email(email)
            if not utils.password.check_password(password, user_entry.hashed_password):
                raise InvalidCredentialsException()
        except UserNotFoundException as e:
            raise InvalidCredentialsException() from e
        return UserToken(
            user_id=user_entry.id,
            exp=datetime.utcnow() + _ACCESS_TOKEN_EXPIRATION,
        )

    def sign_token(self, data: dict) -> str:
        return jwt.encode(
            data,
            os.getenv("ACCESS_TOKEN_SIGNATURE"),
            algorithm=_ACCESS_TOKEN_ALGORITHM,
        )

    def get_authorized_user(self, token: str) -> UserEntry:
        try:
            payload = jwt.decode(
                token,
                os.getenv("ACCESS_TOKEN_SIGNATURE"),
                algorithms=[_ACCESS_TOKEN_ALGORITHM],
            )
            user_token = UserToken(**payload)
        except JWTError as e:
            raise InvalidCredentialsException() from e
        try:
            user_entry = self.user_profile.get_by_id(user_token.user_id)
        except UserNotFoundException as e:
            raise InvalidCredentialsException() from e
        return user_entry


def get_authorized_user(
    token: str = Depends(OAUTH2_SCHEME),
    user_authentication: UserAuthentication = Depends(),
) -> UserEntry:
    return user_authentication.get_authorized_user(token)
