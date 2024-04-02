from fastapi import APIRouter, Depends, status

from src.tasks.schemas import ShowTask, CreateTask, UpdateTask
from src.tasks.service import TaskService
from src.tasks.dependencies import get_task_service
from src.tasks_group.dependencies import valid_owned_tasks
from src.tasks_group.models import TasksGroup

tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@tasks_router.get(
    "/{tasks_group_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[ShowTask],
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
                "application/json": {"example": {"detail": "Task group not found"}}
            },
        },
        406: {
            "content": {"application/json": {"example": {"detail": "User not owner"}}},
        },
    },
)
async def get_tasks(
    tasks_group: TasksGroup = Depends(valid_owned_tasks),
    task_service: TaskService = Depends(get_task_service),
):
    return await task_service.get_from_tasks_group(tasks_group_id=tasks_group.id)


@tasks_router.post(
    "/{tasks_group_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowTask,
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
                "application/json": {"example": {"detail": "Task group not found"}}
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
async def create_task(
    task_data: CreateTask,
    tasks_group: TasksGroup = Depends(valid_owned_tasks),
    task_service: TaskService = Depends(get_task_service),
):
    return await task_service.create(task_data=task_data, tasks_group_id=tasks_group.id)


@tasks_router.patch(
    "/{tasks_group_id}/task/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowTask,
    responses={
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "At least one parameter for task update info should be provided"
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
                "application/json": {
                    "example": {"detail": "Task group or task not found"}
                }
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
async def edit_task(
    task_id: int,
    task_data: UpdateTask,
    tasks_group: TasksGroup = Depends(valid_owned_tasks),
    task_service: TaskService = Depends(get_task_service),
):
    return await task_service.update(task_data=task_data, task_id=task_id)


@tasks_router.delete(
    "/{tasks_group_id}/task/{task_id}",
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
                "application/json": {
                    "example": {"detail": "Task group or task not found"}
                }
            },
        },
        406: {
            "content": {"application/json": {"example": {"detail": "User not owner"}}},
        },
    },
)
async def delete_task(
    task_id: int,
    tasks_group: TasksGroup = Depends(valid_owned_tasks),
    task_service: TaskService = Depends(get_task_service),
):
    return await task_service.delete(task_id=task_id)
