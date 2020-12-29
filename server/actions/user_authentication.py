import os

import bcrypt

_USER_PASSWORD_SECRET = os.getenv("USER_PASSWORD_SECRET")


def _salt(raw_password: str) -> bytes:
    return (_USER_PASSWORD_SECRET + raw_password).encode("utf-8")


def hash_password(raw_password: str) -> bytes:
    return bcrypt.hashpw(_salt(raw_password), bcrypt.gensalt())


def check_password(raw_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(_salt(raw_password), hashed_password)


class UserAuthentication(object):
    pass
