from fastapi import Depends
from sqlalchemy.orm import Session

from actions.user.authentication import hash_password
from actions.internal.user_profile import UserProfile
from data_models.users import UserCreate
from database_schemas.db_session import db_session
from database_schemas.users import UserEntry


class UserAlreadyExistsException(Exception):
    pass


class UserRegistration(object):
    def __init__(
        self, db: Session = Depends(db_session), user_profile: UserProfile = Depends()
    ):
        self.db = db
        self.user_profile = user_profile

    def create_user(self, user: UserCreate) -> UserEntry:
        # ensure user does not exist
        if self.user_profile.find_by_email(user.email):
            raise UserAlreadyExistsException()

        hashed_password = hash_password(user.password)
        user_entry = UserEntry(email=user.email, hashed_password=hashed_password)
        self.db.add(user_entry)
        self.db.commit()
        self.db.refresh(user_entry)
        return user_entry
