from database_schemas.base import Base, engine

Base.metadata.create_all(engine)
