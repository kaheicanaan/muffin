from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr


from actions.user_profile import UserProfile
from actions.user_registration import UserRegistration
from data_models.users import UserCreate, User

router = APIRouter()


@router.post("/", response_model=User)
def create_new_user(
    user: UserCreate,
    user_profile: UserProfile = Depends(),
    user_registration: UserRegistration = Depends(),
):
    db_user = user_profile.find_by_email(email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    return user_registration.create_user(user=user)


@router.get("/{user_email}", response_model=User)
def read_user(user_email: EmailStr, user_profile: UserProfile = Depends()):
    db_user = user_profile.find_by_email(email=user_email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user
