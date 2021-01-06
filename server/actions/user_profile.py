from typing import Optional

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

    # pylint: disable=unsubscriptable-object
    def find_by_id(self, user_id: int) -> Optional[UserEntry]:
        return self.db.query(UserEntry).filter(UserEntry.id == user_id).first()

    # pylint: disable=unsubscriptable-object
    def find_by_email(self, email: str) -> Optional[UserEntry]:
        return self.db.query(UserEntry).filter(UserEntry.email == email).first()
