import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RoomType(enum.Enum):
    chatroom = "CHATROOM"  # with basic E2EE features
    secure_chatroom = "SECURE_CHATROOM"  # with extra security features
    group = "GROUP"
    broadcast = "BROADCAST"
    # other
    self = "SELF"  # chatroom contains user himself only
    system = "SYSTEM"  # Notification from system


class Room(BaseModel):
    id: int
    type: RoomType
    name: str
    description: Optional[str]  # pylint: disable=unsubscriptable-object
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True
