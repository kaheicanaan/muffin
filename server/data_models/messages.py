import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Room(BaseModel):
    id: int
    room_id: int
    user_id: int
    created_at: datetime
    encrypted_message: bytes
    last_updated_at: datetime
    deleted_at: datetime

    class Config:
        orm_mode = True
