from fastapi import Depends
from sqlalchemy.orm import Session

from database_schemas.base import db_session
from database_schemas.users import User as UserTable


class UserProfile(object):
    def __init__(self, db: Session = Depends(db_session)):
        self.db = db

    def find_by_id(self, user_id: str):
        return self.db.query(UserTable).filter(UserTable.id == user_id).first()

    def find_by_email(self, email: str):
        return self.db.query(UserTable).filter(UserTable.email == email).first()
