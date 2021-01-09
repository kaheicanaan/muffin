from datetime import datetime

from pydantic import BaseModel


class UserToken(BaseModel):
    user_id: int
    exp: datetime
