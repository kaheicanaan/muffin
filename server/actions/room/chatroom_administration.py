from fastapi import Depends
from sqlalchemy.orm import Session

from actions.room.base_room_administration import RoomAdministration
from actions.user.profile import UserProfile
from data_models.rooms import RoomType
from database_schemas.db_session import db_session
from database_schemas.participants import ParticipantEntry
from database_schemas.participants import Role
from database_schemas.rooms import RoomEntry


class ChatroomAlreadyExistsException(Exception):
    pass


class ChatroomAdministration(RoomAdministration):
    def __init__(
        self, db: Session = Depends(db_session), user_profile: UserProfile = Depends()
    ):
        super().__init__(db)
        self.db = db
        self.user_profile = user_profile

    def create_room(self, user1_id: int, user2_id: int) -> RoomEntry:
        # ensure users exist
        user1 = self.user_profile.get_by_id(user1_id)
        user2 = self.user_profile.get_by_id(user2_id)

        # check if chatroom exists
        user1_chatroom_ids = {
            room.id for room in user1.rooms if room.type is RoomType.chatroom
        }
        user2_chatroom_ids = {
            room.id for room in user2.rooms if room.type is RoomType.chatroom
        }
        if user1_chatroom_ids & user2_chatroom_ids:
            raise ChatroomAlreadyExistsException()

        # create chatroom and participants
        chatroom_entry = RoomEntry(
            type=RoomType.chatroom,
            name="{user_name}",  # placeholder
        )
        user1_participant_entry = ParticipantEntry(
            user=user1,
            room=chatroom_entry,
            role=Role.member,
        )
        user2_participant_entry = ParticipantEntry(
            user=user2,
            room=chatroom_entry,
            role=Role.member,
        )
        self.db.add_all(
            [chatroom_entry, user1_participant_entry, user2_participant_entry]
        )
        self.db.commit()
        return chatroom_entry
