from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr


from actions.user.authentication import get_authorized_user
from actions.user.profile import UserProfile
from actions.user.registration import (
    UserRegistration,
    EmailAlreadyRegisteredException,
)
from data_models.users import UserCreate, User

router = APIRouter()


@router.post("/", response_model=User)
def create_new_user(
    user: UserCreate,
    user_registration: UserRegistration = Depends(),
):
    try:
        new_user = user_registration.create_user(user=user)
    except EmailAlreadyRegisteredException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered."
        ) from e
    return User.from_orm(new_user)


@router.get(
    "/{user_email}", dependencies=[Depends(get_authorized_user)], response_model=User
)
def read_user(user_email: EmailStr, user_profile: UserProfile = Depends()):
    user = user_profile.find_by_email(email=user_email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return User.from_orm(user)
