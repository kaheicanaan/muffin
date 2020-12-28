from fastapi import Depends
from sqlalchemy.orm import Session

from data_models.users import UserCreate
from database_schemas.base import db_session
from database_schemas.users import User as UserTable


class UserRegistration(object):
    def __init__(self, db: Session = Depends(db_session)):
        self.db = db

    def create_user(self, user: UserCreate):
        hashed_password = user.password  # TODO: Really hash password.
        db_user = UserTable(email=user.email, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
