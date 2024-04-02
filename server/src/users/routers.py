from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.dependencies import get_current_user_from_token
from src.users.service import UserService
from src.users.schemas import ShowUser, UpdateUser, DeletedUser
from src.database_2.models import User


users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=ShowUser,
    responses={
        401: {
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
                }
            }
        },
    },
)
async def read_user(current_user: User = Depends(get_current_user_from_token)):
    return current_user


@users_router.patch(
    "/edit",
    status_code=status.HTTP_200_OK,
    response_model=ShowUser,
    responses={
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
        422: {
            "content": {
                "application/json": {"example": {"detail": "Validation error mesage"}}
            },
        },
    },
)
async def edit_user(
    user_data: UpdateUser, current_user: User = Depends(get_current_user_from_token)
):
    return await UserService().update(user_data=user_data, current_user=current_user)


@users_router.delete(
    "",
    status_code=status.HTTP_200_OK,
    response_model=DeletedUser,
    responses={
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
async def delete_user(current_user: User = Depends(get_current_user_from_token)):
    return await UserService().deactivate(current_user=current_user)
