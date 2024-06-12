from fastapi import APIRouter, Depends, status

from src.responses import InvalidCredentialsException, ValidationException
from src.auth.dependencies import get_current_user_from_token
from src.users.dependencies import get_user_service
from src.users.service import UserService
from src.users.schemas import ShowUser, UpdateUser, DeletedUser
from src.users.models import User
from src.users.responses import UserNotFoundException


users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=ShowUser,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": InvalidCredentialsException}},
)
async def read_user(current_user: User = Depends(get_current_user_from_token)):
    return current_user


@users_router.patch(
    "/edit",
    status_code=status.HTTP_200_OK,
    response_model=ShowUser,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": InvalidCredentialsException},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationException},
        status.HTTP_404_NOT_FOUND: {"model": UserNotFoundException},
    },
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
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": InvalidCredentialsException},
        status.HTTP_404_NOT_FOUND: {"model": UserNotFoundException},
    },
)
async def delete_user(
    current_user: User = Depends(get_current_user_from_token),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.deactivate(current_user=current_user)
