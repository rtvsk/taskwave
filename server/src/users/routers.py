from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import get_current_user_from_token
from src.users.models import Users
from src.users.service import UsersService
from src.users.dependencies import users_service
from src.users.exceptions import UserNotFound, UserAlreadyExists
from src.users.schemas import CreateUser, ShowUser, UpdateUser, DeletedUser


users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post(
    "/singup",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"model": ShowUser},
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User with this login or email already exists"
                    }
                }
            },
        },
        422: {
            "content": {
                "application/json": {"example": {"detail": "Validation error mesage"}}
            },
        },
    },
)
async def create_user(
    new_user: CreateUser,
    users_service: UsersService = Depends(users_service),
):
    try:
        return await users_service.create(user_data=new_user)
    except UserAlreadyExists as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{ex}")


@users_router.get(
    "/me",
    responses={
        200: {"model": ShowUser},
        401: {
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
                }
            }
        },
    },
)
async def read_user(
    current_user: Users = Depends(get_current_user_from_token),
):
    return current_user


@users_router.patch(
    "/edit",
    responses={
        200: {"model": ShowUser},
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "At least one parameter for user update info should be provided"
                    }
                }
            }
        },
        401: {
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
                }
            }
        },
    },
)
async def edit_user(
    user_data: UpdateUser,
    current_user: Users = Depends(get_current_user_from_token),
    users_service: UsersService = Depends(users_service),
):
    try:
        return await users_service.update(
            user_data=user_data,
            current_user=current_user,
        )
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{ex}")


@users_router.delete("", status_code=status.HTTP_200_OK, response_model=DeletedUser)
async def delete_user(
    current_user: Users = Depends(get_current_user_from_token),
    users_service: UsersService = Depends(users_service),
):
    try:
        return await users_service.deactivate(current_user=current_user)
    except UserNotFound as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{ex}")
