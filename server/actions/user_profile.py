from fastapi import Depends

from database_schemas.base import DBSession
from database_schemas.users import User as UserTable


class UserProfile(object):
    def __init__(self, db: DBSession = Depends()):
        # TODO: Make this more elegant, i.e. self.db = db would be sufficient.
        self.db = db.db

    def find_by_id(self, user_id: str):
        return self.db.query(UserTable).filter(UserTable.id == user_id).first()

    def find_by_email(self, email: str):
        return self.db.query(UserTable).filter(
            UserTable.email == email).first()
