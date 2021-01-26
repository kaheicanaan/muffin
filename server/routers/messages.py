from fastapi import APIRouter, Depends, HTTPException, status

from actions.room.base_room_administration import (
    RoomNotFoundException,
    ParticipantNotFoundException,
)
from actions.room.message_crud import MessageCRUD, NoMessageCreationAccessException
from actions.user.authentication import get_authorized_user
from data_models.messages import Message
from database_schemas.users import UserEntry

router = APIRouter()


@router.post("/", response_model=Message)
def create_message(
    room_id: int,
    encrypted_message: str,
    user: UserEntry = Depends(get_authorized_user),
    message_crud: MessageCRUD = Depends(),
):
    try:
        new_message = message_crud.create_message(user.id, room_id, encrypted_message)
    except RoomNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room does not exist.",
        ) from e
    except ParticipantNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not belong to this room.",
        ) from e
    except NoMessageCreationAccessException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access right to create message.",
        ) from e
    return Message.from_orm(new_message)
