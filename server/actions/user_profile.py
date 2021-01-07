from fastapi import Depends
from sqlalchemy.orm import Session

from database_schemas.db_session import db_session
from database_schemas.users import UserEntry


class UserNotFoundException(Exception):
    def __init__(self, user_id: int = None, user_email: str = None):
        super().__init__()
        self.user_id = user_id
        self.user_email = user_email


class UserProfile(object):
    def __init__(self, db: Session = Depends(db_session)):
        self.db = db

    def find_by_id(self, user_id: int) -> UserEntry:
        user_entry = self.db.query(UserEntry).filter(UserEntry.id == user_id).first()
        if user_entry is None:
            raise UserNotFoundException(user_id=user_id)
        return user_entry

    def find_by_email(self, email: str) -> UserEntry:
        user_entry = self.db.query(UserEntry).filter(UserEntry.email == email).first()
        if user_entry is None:
            raise UserNotFoundException(user_email=email)
        return user_entry
