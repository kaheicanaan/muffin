from fastapi import Depends
from sqlalchemy.orm import Session

from actions.user_profile import UserProfile, UserNotFoundException
from data_models.rooms import RoomType
from database_schemas.db_session import db_session
from database_schemas.participants import ParticipantEntry
from database_schemas.participants import Role
from database_schemas.rooms import RoomEntry


class ChatroomAdministration(object):
    def __init__(
        self, db: Session = Depends(db_session), user_profile: UserProfile = Depends()
    ):
        self.db = db
        self.user_profile = user_profile

    def create_chatroom(self, my_user_id: int, their_user_id: int) -> RoomEntry:
        # ensure users exist
        me = self.user_profile.find_by_id(my_user_id)
        if me is None:
            raise UserNotFoundException(user_id=my_user_id)
        they = self.user_profile.find_by_id(their_user_id)
        if they is None:
            raise UserNotFoundException(user_id=their_user_id)

        # TODO: ensure chatroom does not exist

        chatroom_entry = RoomEntry(
            type=RoomType.chatroom,
            name="{user_name}",  # placeholder
        )
        # self.db.add(chatroom_entry)
        # self.db.commit()
        # self.db.refresh(chatroom_entry)
        # room_id = chatroom_entry.id

        my_participant_entry = ParticipantEntry(
            user=me,
            room=chatroom_entry,
            role=Role.member,
        )
        their_participant_entry = ParticipantEntry(
            user=they,
            room=chatroom_entry,
            role=Role.member,
        )
        self.db.add_all([chatroom_entry, my_participant_entry, their_participant_entry])
        self.db.commit()
        return chatroom_entry
