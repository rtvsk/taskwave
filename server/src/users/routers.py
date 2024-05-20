from fastapi import APIRouter, Depends, status

from src.auth.dependencies import get_current_user_from_token
from src.auth.responses import credentials_error_response
from src.users.dependencies import get_user_service
from src.users.service import UserService
from src.users.schemas import ShowUser, UpdateUser, DeletedUser
from src.users.models import User
from src.users.responses import users_edit_responses


users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=ShowUser,
    responses={**credentials_error_response},
)
async def read_user(current_user: User = Depends(get_current_user_from_token)):
    return current_user


@users_router.patch(
    "/edit",
    status_code=status.HTTP_200_OK,
    response_model=ShowUser,
    responses={**users_edit_responses},
)
async def edit_user(
    user_data: UpdateUser,
    current_user: User = Depends(get_current_user_from_token),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.update_user(
        user_data=user_data, current_user=current_user
    )


@users_router.delete(
    "",
    status_code=status.HTTP_200_OK,
    response_model=DeletedUser,
    responses={**credentials_error_response},
)
async def delete_user(
    current_user: User = Depends(get_current_user_from_token),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.deactivate(current_user=current_user)
