from fastapi import Depends
from sqlalchemy.orm import Session

from actions.internal.chatroom_administration import ChatroomAdministration
from data_models.rooms import RoomType
from database_schemas.db_session import db_session
from database_schemas.messages import MessageEntry
from database_schemas.participants import Role


class NoMessageCreationAccessException(Exception):
    def __init__(self, user_id: int, room_id: int, role: Role):
        super().__init__()
        self.user_id = user_id
        self.room_id = room_id
        self.role = role


SEND_MESSAGE_ACCESS_CONTROL = {
    RoomType.chatroom: {Role.member}  # member is the only available role in chatroom
}


class MessageCRUD(object):
    def __init__(
        self,
        db: Session = Depends(db_session),
        chatroom_administration: ChatroomAdministration = Depends(),
    ):
        self.db = db
        self.chatroom_administration = chatroom_administration

    def create_message(
        self, user_id: int, room_id: int, encrypted_message: str
    ) -> MessageEntry:
        # check user access right before create message
        room = self.chatroom_administration.get_room_by_id(room_id)
        role = self.chatroom_administration.get_user_role(room_id, user_id)
        if role not in SEND_MESSAGE_ACCESS_CONTROL[room.type]:
            raise NoMessageCreationAccessException(user_id, room_id, role)

        # create message record
        message_entry = MessageEntry(
            room_id=room_id, user_id=user_id, encrypted_message=encrypted_message
        )
        self.db.add(message_entry)
        self.db.commit()
        self.db.refresh(message_entry)
        return message_entry
