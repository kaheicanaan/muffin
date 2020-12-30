import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def postgres_db_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


TEST_SQLALCHEMY_DATABASE_URL = "sqlite://"

test_engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
SQLiteSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def sqlite_db_session():
    try:
        db = SQLiteSessionLocal()
        yield db
    finally:
        db.close()


# As dependency argument, i.e. `db: Session = Depends(db_session)`, where test may override by
# `app.dependency_overrides[db_session] = test_db_session`.
db_session = postgres_db_session
