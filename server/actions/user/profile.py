from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from actions import utils
from database_schemas.db_session import db_session
from database_schemas.users import UserEntry


class UserNotFoundException(Exception):
    def __init__(
        self, user_id: int = None, username: str = None, user_email: str = None
    ):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.user_email = user_email


class EmailAlreadyUsedException(Exception):
    def __init__(self, user_email: str = None):
        super().__init__()
        self.user_email = user_email


class UsernameAlreadyUsedException(Exception):
    def __init__(self, username: str = None):
        super().__init__()
        self.username = username


class UserProfile(object):
    def __init__(self, db: Session = Depends(db_session)):
        self.db = db

    # pylint: disable=unsubscriptable-object
    def find_by_id(self, user_id: int) -> Optional[UserEntry]:
        return self.db.query(UserEntry).filter(UserEntry.id == user_id).first()

    def get_by_id(self, user_id: int) -> UserEntry:
        user_entry = self.find_by_id(user_id)
        if user_entry is None:
            raise UserNotFoundException(user_id=user_id)
        return user_entry

    # pylint: disable=unsubscriptable-object
    def find_by_username(self, username: str) -> Optional[UserEntry]:
        return self.db.query(UserEntry).filter(UserEntry.username == username).first()

    def get_by_username(self, username: str) -> UserEntry:
        user_entry = self.find_by_username(username)
        if user_entry is None:
            raise UserNotFoundException(username=username)
        return user_entry

    def update_username(self, user_id: int, new_username: str) -> UserEntry:
        user_entry = self.get_by_id(user_id)
        # check if email duplicated
        other_user_entry = self.find_by_username(new_username)
        if other_user_entry:
            raise UsernameAlreadyUsedException(username=new_username)

        # update
        user_entry.username = new_username
        self.db.commit()
        return user_entry

    # pylint: disable=unsubscriptable-object
    def find_by_email(self, email: str) -> Optional[UserEntry]:
        return self.db.query(UserEntry).filter(UserEntry.email == email).first()

    def get_by_email(self, email: str) -> UserEntry:
        user_entry = self.find_by_email(email)
        if user_entry is None:
            raise UserNotFoundException(user_email=email)
        return user_entry

    def update_email(self, user_id: int, new_email: str) -> UserEntry:
        user_entry = self.get_by_id(user_id)
        # check if email duplicated
        other_user_entry = self.find_by_email(new_email)
        if other_user_entry:
            raise EmailAlreadyUsedException(user_email=new_email)

        # update
        user_entry.email = new_email
        self.db.commit()
        return user_entry

    def update_password(self, user_id: int, new_password: str) -> UserEntry:
        user_entry = self.get_by_id(user_id)
        hashed_password = utils.password.hash_password(new_password)
        user_entry.hashed_password = hashed_password
        self.db.commit()
        return user_entry
