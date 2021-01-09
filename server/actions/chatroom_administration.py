from fastapi import Depends
from sqlalchemy.orm import Session

from actions.user_profile import UserProfile
from data_models.rooms import RoomType
from database_schemas.db_session import db_session
from database_schemas.participants import ParticipantEntry
from database_schemas.participants import Role
from database_schemas.rooms import RoomEntry


class RoomNotFoundException(Exception):
    pass


class ChatroomAlreadyExistsException(Exception):
    pass


class ParticipantNotFoundException(Exception):
    pass


class ChatroomAdministration(object):
    def __init__(
        self, db: Session = Depends(db_session), user_profile: UserProfile = Depends()
    ):
        self.db = db
        self.user_profile = user_profile

    def create_chatroom(self, my_user_id: int, their_user_id: int) -> RoomEntry:
        # ensure users exist
        me = self.user_profile.get_by_id(my_user_id)
        they = self.user_profile.get_by_id(their_user_id)

        my_chatroom_ids = {
            room.id for room in me.rooms if room.type is RoomType.chatroom
        }
        they_chatroom_ids = {
            room.id for room in they.rooms if room.type is RoomType.chatroom
        }
        if my_chatroom_ids & they_chatroom_ids:
            raise ChatroomAlreadyExistsException()

        chatroom_entry = RoomEntry(
            type=RoomType.chatroom,
            name="{user_name}",  # placeholder
        )

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

    def get_room(self, room_id: int) -> RoomEntry:
        room_entry = self.db.query(RoomEntry).filter(RoomEntry.id == room_id).first()
        if room_entry is None:
            raise RoomNotFoundException()
        return room_entry

    def get_user_role(self, room_id: int, user_id: int) -> Role:
        participant: ParticipantEntry = (
            self.db.query(ParticipantEntry)
            .filter(
                (ParticipantEntry.room_id == room_id)
                & (ParticipantEntry.user_id == user_id)
            )
            .first()
        )
        if participant is None:
            raise ParticipantNotFoundException()
        return participant.role
