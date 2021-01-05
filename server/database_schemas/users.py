from sqlalchemy import Boolean, Column, LargeBinary, Integer, String

from database_schemas.base import Base


class UserEntry(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(LargeBinary)
    is_active = Column(Boolean, default=True)
