from fastapi import Depends
from sqlalchemy.orm import Session

from actions import utils
from actions.user.profile import UserProfile
from data_models.users import UserCreate
from database_schemas.db_session import db_session
from database_schemas.users import UserEntry


class UsernameAlreadyRegisteredException(Exception):
    pass


class EmailAlreadyRegisteredException(Exception):
    pass


class UserRegistration(object):
    def __init__(
        self, db: Session = Depends(db_session), user_profile: UserProfile = Depends()
    ):
        self.db = db
        self.user_profile = user_profile

    def create_user(self, user: UserCreate) -> UserEntry:
        # ensure username and email do not exist
        if self.user_profile.find_by_username(user.username):
            raise UsernameAlreadyRegisteredException()
        if self.user_profile.find_by_email(user.email):
            raise EmailAlreadyRegisteredException()

        hashed_password = utils.password.hash_password(user.password)
        user_entry = UserEntry(
            username=user.username, email=user.email, hashed_password=hashed_password
        )
        self.db.add(user_entry)
        self.db.commit()
        self.db.refresh(user_entry)
        return user_entry
