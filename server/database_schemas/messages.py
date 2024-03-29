from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)

from database_schemas.base import Base


class MessageEntry(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    encrypted_message = Column(String, nullable=False)
    last_updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    UniqueConstraint(room_id, created_at)
