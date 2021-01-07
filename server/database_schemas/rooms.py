from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship

from data_models.rooms import RoomType
from database_schemas.base import Base


class RoomEntry(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(Enum(RoomType), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    created_time = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    users = relationship("UserEntry", secondary="participants", back_populates="rooms")
