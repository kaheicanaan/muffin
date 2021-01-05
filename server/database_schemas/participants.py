import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database_schemas.base import Base


class Role(enum.Enum):
    member = "MEMBER"
    owner = "OWNER"
    admin = "ADMIN"
    announcer = "ANNOUNCER"


class ParticipantEntry(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), index=True)
    role = Column(Enum(Role), nullable=False)

    user = relationship("UserEntry", back_populates="rooms")
    room = relationship("RoomEntry", back_populates="users")
