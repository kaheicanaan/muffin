import pytest

from actions.chatroom_administration import (
    RoomNotFoundException,
    ParticipantNotFoundException,
)
from actions.message_crud import MessageCRUD
from database_schemas.rooms import RoomEntry
from database_schemas.users import UserEntry


class TestSendMessageToChatroom(object):
    def test_send_message_to_room_does_not_exist(
        self,
        message_crud: MessageCRUD,
        user_entry_squirtle: UserEntry,
    ):
        non_exist_room_id = 42
        with pytest.raises(RoomNotFoundException):
            message_crud.create_message(
                user_entry_squirtle.id, non_exist_room_id, "ping"
            )

    def test_send_message_by_irrelevant_user(
        self,
        message_crud: MessageCRUD,
        pokemon_chatroom: RoomEntry,
        user_entry_pusheen: UserEntry,
    ):
        with pytest.raises(ParticipantNotFoundException):
            message_crud.create_message(
                user_entry_pusheen.id, pokemon_chatroom.id, "Hey"
            )

    def test_send_message_by_room_members(
        self,
        message_crud: MessageCRUD,
        pokemon_chatroom: RoomEntry,
        user_entry_squirtle: UserEntry,
        user_entry_zenigame: UserEntry,
    ):
        msg_1 = message_crud.create_message(
            user_entry_squirtle.id, pokemon_chatroom.id, "How are you?"
        )
        assert isinstance(msg_1.id, int)
        msg_2 = message_crud.create_message(
            user_entry_zenigame.id, pokemon_chatroom.id, "Fine. Thank you."
        )
        assert msg_2.id > msg_1.id
