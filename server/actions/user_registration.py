from fastapi import Depends
from sqlalchemy.orm import Session

from actions.user_profile import UserProfile
from data_models.users import User, UserCreate
from database_schemas.base import db_session
from database_schemas.users import UserEntry


class UserAlreadyExistsException(Exception):
    pass


class UserRegistration(object):
    def __init__(
        self, db: Session = Depends(db_session), user_profile: UserProfile = Depends()
    ):
        self.db = db
        self.user_profile = user_profile

    def create_user(self, user: UserCreate) -> User:
        if self.user_profile.find_by_email(user.email):
            raise UserAlreadyExistsException()
        hashed_password = user.password  # TODO: Really hash password.
        user_entry = UserEntry(email=user.email, hashed_password=hashed_password)
        self.db.add(user_entry)
        self.db.commit()
        self.db.refresh(user_entry)
        return User.from_orm(user_entry)
