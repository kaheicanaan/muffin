import pytest

from actions.room.base_room_administration import RoomAdministration
from actions.room.chatroom_administration import ChatroomAdministration
from actions.room.message_crud import MessageCRUD
from actions.user.profile import UserProfile
from actions.user.registration import UserRegistration
from data_models.users import UserCreate
from database_schemas.base import Base
from database_schemas.db_session import sqlite_db_session, test_engine
from database_schemas.users import UserEntry


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ACCESS_TOKEN_SIGNATURE", "SIGN")
    monkeypatch.setenv("USER_PASSWORD_SECRET", "SECRET")


@pytest.fixture(name="db")
def fixture_db():
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    return next(sqlite_db_session())


# Actions
@pytest.fixture(name="user_profile")
def fixture_user_profile(db) -> UserProfile:
    return UserProfile(db)


@pytest.fixture(name="user_registration")
def fixture_user_registration(db, user_profile) -> UserRegistration:
    return UserRegistration(db, user_profile)


@pytest.fixture(name="room_administration")
def fixture_room_administration(db) -> RoomAdministration:
    return ChatroomAdministration(db)


@pytest.fixture(name="chatroom_administration")
def fixture_chatroom_administration(db, user_profile) -> ChatroomAdministration:
    return ChatroomAdministration(db, user_profile)


@pytest.fixture(name="message_crud")
def fixture_message_crud(db, room_administration) -> MessageCRUD:
    return MessageCRUD(db, room_administration)


# Dummy Users
@pytest.fixture(name="user_create_squirtle")
def fixture_user_create_squirtle() -> UserCreate:
    return UserCreate(
        **{
            "username": "squirtle",
            "email": "squirtle@example.com",
            "password": "password",
        }
    )


@pytest.fixture(name="user_entry_squirtle")
def fixture_user_entry_squirtle(user_registration, user_create_squirtle) -> UserEntry:
    return user_registration.create_user(user_create_squirtle)


@pytest.fixture(name="user_create_zenigame")
def fixture_user_create_zenigame() -> UserCreate:
    return UserCreate(
        **{
            "username": "zenigame",
            "email": "zenigame@example.com",
            "password": "Password",
        }
    )


@pytest.fixture(name="user_entry_zenigame")
def fixture_user_entry_zenigame(user_registration, user_create_zenigame) -> UserEntry:
    return user_registration.create_user(user_create_zenigame)


@pytest.fixture(name="user_create_pusheen")
def fixture_user_create_pusheen() -> UserCreate:
    return UserCreate(
        **{
            "username": "pusheen",
            "email": "pusheen@example.com",
            "password": "pussword",
        }
    )


@pytest.fixture(name="user_entry_pusheen")
def fixture_user_entry_pusheen(user_registration, user_create_pusheen) -> UserEntry:
    return user_registration.create_user(user_create_pusheen)


# Dummy Rooms
@pytest.fixture(name="pokemon_chatroom")
def fixture_pokemon_chatroom(
    user_entry_squirtle, user_entry_zenigame, chatroom_administration
):
    return chatroom_administration.create_room(
        user_entry_squirtle.id, user_entry_zenigame.id
    )
