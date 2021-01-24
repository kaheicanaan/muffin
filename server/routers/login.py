from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from actions.user.authentication import (
    UserAuthentication,
    InvalidCredentialsException,
)

router = APIRouter()


@router.post("/")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_authentication: UserAuthentication = Depends(),
) -> str:
    try:
        user_token = user_authentication.login(
            email=form_data.username, password=form_data.password
        )
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials.",
        ) from e
    return {
        "access_token": user_authentication.sign_token(user_token.dict()),
        "token_type": "bearer",
    }
