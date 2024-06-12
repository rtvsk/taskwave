from fastapi import APIRouter, Depends, status

from src.responses import InvalidCredentialsException, ValidationException
from src.tasks.schemas import ShowTask, CreateTask, UpdateTask
from src.tasks.service import TaskService
from src.tasks.models import Task
from src.tasks.responses import TaskNotFoundException
from src.tasks.dependencies import get_task_service, valid_tasks_group
from src.tasks_group.dependencies import valid_owned_tasks
from src.tasks_group.models import TasksGroup
from src.tasks_group.responses import TaskGroupNotFoundException, UserNotOwnerException


tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@tasks_router.get(
    "/{tasks_group_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[ShowTask],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": InvalidCredentialsException},
        status.HTTP_404_NOT_FOUND: {"model": TaskGroupNotFoundException},
        status.HTTP_406_NOT_ACCEPTABLE: {"model": UserNotOwnerException},
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
        status.HTTP_401_UNAUTHORIZED: {"model": InvalidCredentialsException},
        status.HTTP_404_NOT_FOUND: {"model": TaskGroupNotFoundException},
        status.HTTP_406_NOT_ACCEPTABLE: {"model": UserNotOwnerException},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationException},
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
        status.HTTP_401_UNAUTHORIZED: {"model": InvalidCredentialsException},
        status.HTTP_404_NOT_FOUND: {"model": TaskNotFoundException},
        status.HTTP_406_NOT_ACCEPTABLE: {"model": UserNotOwnerException},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationException},
    },
)
async def edit_task(
    task_data: UpdateTask,
    task: Task = Depends(valid_tasks_group),
    task_service: TaskService = Depends(get_task_service),
):
    return await task_service.update_task(task_data=task_data, task_id=task.id)


@tasks_router.delete(
    "/{tasks_group_id}/task/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": InvalidCredentialsException},
        status.HTTP_404_NOT_FOUND: {"model": TaskNotFoundException},
        status.HTTP_406_NOT_ACCEPTABLE: {"model": UserNotOwnerException},
    },
)
async def delete_task(
    task: Task = Depends(valid_tasks_group),
    task_service: TaskService = Depends(get_task_service),
):
    return await task_service.delete_task(task_id=task.id)
