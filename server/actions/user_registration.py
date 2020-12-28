from fastapi import Depends

from data_models.users import UserCreate
from database_schemas.base import DBSession
from database_schemas.users import User as UserTable


class UserRegistration(object):
    def __init__(self, db: DBSession = Depends()):
        # TODO: Make this more elegant, i.e. self.db = db would be sufficient.
        self.db = db.db

    def create_user(self, user: UserCreate):
        hashed_password = user.password  # TODO: Really hash password.
        db_user = UserTable(email=user.email, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
