from sqlalchemy import Column, Enum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from data_models.participants import Role
from database_schemas.base import Base


class ParticipantEntry(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), index=True)
    role = Column(Enum(Role), nullable=False)

    user = relationship("UserEntry")
    room = relationship("RoomEntry")

    UniqueConstraint(user_id, room_id)
