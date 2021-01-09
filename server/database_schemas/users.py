from sqlalchemy import Boolean, Column, LargeBinary, Integer, String
from sqlalchemy.orm import relationship

from database_schemas.base import Base


class UserEntry(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(LargeBinary)
    is_active = Column(Boolean, default=True)

    rooms = relationship("RoomEntry", secondary="participants", back_populates="users")
