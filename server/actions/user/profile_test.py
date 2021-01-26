import pytest

from actions.user.profile import UserProfile, UserNotFoundException
from database_schemas.users import UserEntry


class TestGetProfile(object):
    def test_get_existing_user_by_id(
        self,
        user_profile: UserProfile,
        user_entry_squirtle: UserEntry,
    ):
        squirtle = user_profile.get_by_id(user_entry_squirtle.id)
        assert user_entry_squirtle == squirtle

    def test_get_user_by_non_exist_id(
        self,
        user_profile: UserProfile,
    ):
        with pytest.raises(UserNotFoundException):
            user_profile.get_by_id(4242)


class TestUpdateProfile(object):
    def test_update_email(
        self,
        user_profile: UserProfile,
        user_entry_squirtle: UserEntry,
    ):
        old_email = user_entry_squirtle.email
        new_email = "new_email@example.com"
        _ = user_profile.update_email(user_entry_squirtle.id, new_email)
        assert user_entry_squirtle.email != old_email
        assert user_entry_squirtle.email == new_email

    def test_update_password(
        self,
        user_profile: UserProfile,
        user_entry_squirtle: UserEntry,
    ):
        old_hashed_password = user_entry_squirtle.hashed_password
        new_password = "new_password"
        _ = user_profile.update_password(user_entry_squirtle.id, new_password)
        assert user_entry_squirtle.hashed_password != old_hashed_password
