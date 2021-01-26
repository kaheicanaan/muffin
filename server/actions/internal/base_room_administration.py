import abc

from fastapi import Depends
from sqlalchemy.orm import Session

from database_schemas.db_session import db_session
from database_schemas.participants import ParticipantEntry
from database_schemas.participants import Role
from database_schemas.rooms import RoomEntry


class RoomNotFoundException(Exception):
    pass


class ParticipantNotFoundException(Exception):
    pass


class RoomAdministration(abc.ABC):
    def __init__(self, db: Session = Depends(db_session)):
        self.db = db

    @abc.abstractmethod
    def create_room(self, user1_id: int, user2_id: int) -> RoomEntry:
        pass

    def get_room_by_id(self, room_id: int) -> RoomEntry:
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
