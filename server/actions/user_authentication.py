import base64
import hashlib
import logging
import os

import bcrypt

logger = logging.getLogger(__name__)

_USER_PASSWORD_SECRET = os.getenv("USER_PASSWORD_SECRET", "")


def _pepper(raw_password: str) -> bytes:
    return base64.b64encode(
        hashlib.sha256((raw_password + _USER_PASSWORD_SECRET).encode("utf-8")).digest()
    )


def hash_password(raw_password: str) -> bytes:
    return bcrypt.hashpw(_pepper(raw_password), bcrypt.gensalt())


def check_password(raw_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(_pepper(raw_password), hashed_password)


class UserAuthentication(object):
    pass
