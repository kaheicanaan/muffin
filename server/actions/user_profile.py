from fastapi import Depends
from sqlalchemy.orm import Session

from data_models.users import User
from database_schemas.base import db_session
from database_schemas.users import UserEntry


class UserProfile(object):
    def __init__(self, db: Session = Depends(db_session)):
        self.db = db

    def find_by_id(self, user_id: str) -> User:
        user_entry = self.db.query(UserEntry).filter(UserEntry.id == user_id).first()
        return User.from_orm(user_entry) if user_entry else None

    def find_by_email(self, email: str) -> User:
        user_entry = self.db.query(UserEntry).filter(UserEntry.email == email).first()
        return User.from_orm(user_entry) if user_entry else None
