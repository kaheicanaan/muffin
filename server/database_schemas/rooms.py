import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String

from .base import Base


class RoomType(enum.Enum):
    chatroom = "Chatroom"  # with basic E2EE features
    secure_chatroom = "Secure Chatroom"  # with extra security features
    group = "Group"
    pub_sub = "Pub Sub"
    # other
    self = "Self"  # chatroom contains user himself only
    admin = "Admin"  # Notification from system admin


class RoomEntry(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(Enum(RoomType), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_time = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
