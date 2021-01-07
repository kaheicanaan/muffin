import pytest

from actions.chatroom_administration import (
    ChatroomAdministration,
    ChatroomAlreadyExistsException,
)
from database_schemas.users import UserEntry


class TestCreateChatroom(object):
    def test_new_chatroom(
        self,
        chatroom_administration: ChatroomAdministration,
        user_entry_squirtle: UserEntry, user_entry_zenigame: UserEntry,
    ):
        new_chatroom = chatroom_administration.create_chatroom(
            user_entry_squirtle.id, user_entry_zenigame.id
        )
        assert isinstance(new_chatroom.id, int)

    def test_existing_chatroom(
        self,
        chatroom_administration: ChatroomAdministration,
        user_entry_squirtle: UserEntry,
        user_entry_zenigame: UserEntry,
    ):
        new_chatroom = chatroom_administration.create_chatroom(
            user_entry_squirtle.id, user_entry_zenigame.id
        )
        assert isinstance(new_chatroom.id, int)
        with pytest.raises(ChatroomAlreadyExistsException):
            chatroom_administration.create_chatroom(
                user_entry_squirtle.id, user_entry_zenigame.id
            )
