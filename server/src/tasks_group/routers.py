from fastapi import APIRouter, Depends, status

from src.auth.dependencies import get_current_user_from_token
from src.tasks_group.schemas import CreateTasksGroup, ShowTasksGroup, UpdateTasksGroup
from src.tasks_group.service import TasksGroupService
from src.tasks_group.dependencies import valid_owned_tasks

from src.database_2.models import User, TasksGroup

tasks_group_router = APIRouter(prefix="/tasks", tags=["Tasks_group"])


@tasks_group_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[ShowTasksGroup],
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
async def users_tasks_group(
    current_user: User = Depends(get_current_user_from_token),
):
    return await TasksGroupService().get_all_from_user(author_id=current_user.id)


@tasks_group_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowTasksGroup,
    responses={
        401: {
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
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
async def create_tasks_group(
    tasks_group_data: CreateTasksGroup,
    current_user: User = Depends(get_current_user_from_token),
):
    return await TasksGroupService().create(
        tasks_group_data=tasks_group_data, author_id=current_user.id
    )


@tasks_group_router.patch(
    "/{tasks_group_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowTasksGroup,
    responses={
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "At least one parameter for tasks group update info should be provided"
                    }
                }
            },
        },
        401: {
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
                }
            },
        },
        404: {
            "content": {
                "application/json": {"example": {"detail": "Tasks group not found"}}
            },
        },
        406: {
            "content": {"application/json": {"example": {"detail": "User not owner"}}},
        },
        422: {
            "content": {
                "application/json": {"example": {"detail": "Validation error mesage"}}
            },
        },
    },
)
async def edit_tasks_group(
    tasks_group_data: UpdateTasksGroup,
    tasks_group: TasksGroup = Depends(valid_owned_tasks),
):
    return await TasksGroupService().update(
        tasks_group_id=tasks_group.id, tasks_group_data=tasks_group_data
    )


@tasks_group_router.delete(
    "/{tasks_group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
                }
            },
        },
        404: {
            "content": {
                "application/json": {"example": {"detail": "Tasks group not found"}}
            },
        },
        406: {
            "content": {"application/json": {"example": {"detail": "User not owner"}}},
        },
    },
)
async def delete_tasks_group(tasks_group: TasksGroup = Depends(valid_owned_tasks)):
    return await TasksGroupService().delete(tasks_group_id=tasks_group.id)
