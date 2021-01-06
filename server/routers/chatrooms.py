from fastapi import APIRouter, Depends, HTTPException, status

from actions.chatroom_administration import ChatroomAdministration
from actions.user_profile import UserNotFoundException
from data_models.rooms import Room

router = APIRouter()


@router.post("/", response_model=Room)
def create_chatroom(
    user_id_1: int,
    user_id_2: int,
    chatroom_admin: ChatroomAdministration = Depends(),
):
    try:
        new_chatroom = chatroom_admin.create_chatroom(user_id_1, user_id_2)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User ID {e.user_id} does not exist.",
        ) from e
    return Room.from_orm(new_chatroom)
