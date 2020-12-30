from database_schemas.base import Base
from database_schemas.db_session import engine

Base.metadata.create_all(engine)
