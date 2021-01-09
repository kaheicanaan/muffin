from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    id: int
    room_id: int
    user_id: int
    created_at: datetime
    encrypted_message: str
    last_updated_at: Optional[datetime]  # pylint: disable=unsubscriptable-object
    deleted_at: Optional[datetime]  # pylint: disable=unsubscriptable-object

    class Config:
        orm_mode = True
