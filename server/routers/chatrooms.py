from fastapi import APIRouter, Depends, HTTPException, status

from actions.internal.chatroom_administration import (
    ChatroomAdministration,
    ChatroomAlreadyExistsException,
)
from actions.internal.user_profile import UserNotFoundException
from actions.user.authentication import get_authorized_user
from data_models.rooms import Room
from database_schemas.users import UserEntry

router = APIRouter()


@router.post("/", response_model=Room)
def create_chatroom(
    other_user_id: int,  # TODO: change to username
    user: UserEntry = Depends(get_authorized_user),
    chatroom_admin: ChatroomAdministration = Depends(),
):
    try:
        new_chatroom = chatroom_admin.create_room(user.id, other_user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User ID {e.user_id} does not exist.",
        ) from e
    except ChatroomAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Chatroom already exists.",
        ) from e
    return Room.from_orm(new_chatroom)
