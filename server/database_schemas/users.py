from sqlalchemy import Boolean, Binary, Column, Integer, String

from database_schemas.base import Base


class UserEntry(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(Binary)
    is_active = Column(Boolean, default=True)
