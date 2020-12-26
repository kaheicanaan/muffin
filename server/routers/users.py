from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from ..data_models.users import UserCreate
from ..database_schemas.base import get_db_session
from ..database_schemas.users import User as UserTable


# CREATE
def create_user(db: Session, user: UserCreate):
    hashed_password = user.password  # TODO: hash password
    db_user = UserTable(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# READ
def get_user_by_id(db: Session, user_id: str):
    return db.query(UserTable).filter(UserTable.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(UserTable).filter(UserTable.email == email).first()


def count_users(db: Session):
    return db.query(UserTable).count()


# Endpoints
router = APIRouter()


@router.get("/{user_id}")
async def read_user(user_id: str, db: Session = Depends(get_db_session)):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
