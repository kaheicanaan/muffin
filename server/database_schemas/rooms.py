import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship

from database_schemas.base import Base


class RoomType(enum.Enum):
    chatroom = "CHATROOM"  # with basic E2EE features
    secure_chatroom = "SECURE_CHATROOM"  # with extra security features
    group = "GROUP"
    broadcast = "BROADCAST"
    # other
    self = "SELF"  # chatroom contains user himself only
    system = "SYSTEM"  # Notification from system


class RoomEntry(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(Enum(RoomType), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_time = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    users = relationship("ParticipantEntry", back_populates="room")
