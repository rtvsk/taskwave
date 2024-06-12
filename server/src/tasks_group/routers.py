from fastapi import APIRouter, Depends, status

from src.responses import InvalidCredentialsException, ValidationException
from src.auth.dependencies import get_current_user_from_token
from src.tasks_group.responses import TaskGroupNotFoundException, UserNotOwnerException
from src.tasks_group.models import TasksGroup
from src.tasks_group.schemas import CreateTasksGroup, ShowTasksGroup, UpdateTasksGroup
from src.tasks_group.service import TasksGroupService
from src.tasks_group.dependencies import valid_owned_tasks, get_tasks_group_service
from src.users.models import User


tasks_group_router = APIRouter(prefix="/tasks", tags=["Tasks_group"])


@tasks_group_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[ShowTasksGroup],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": InvalidCredentialsException},
    },
)
async def users_tasks_group(
    current_user: User = Depends(get_current_user_from_token),
    tasks_group_service: TasksGroupService = Depends(get_tasks_group_service),
):
    return await tasks_group_service.get_all_from_user(author_id=current_user.id)


@tasks_group_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowTasksGroup,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": InvalidCredentialsException},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationException},
    },
)
async def create_tasks_group(
    tasks_group_data: CreateTasksGroup,
    current_user: User = Depends(get_current_user_from_token),
    tasks_group_service: TasksGroupService = Depends(get_tasks_group_service),
):
    return await tasks_group_service.create(
        tasks_group_data=tasks_group_data, author_id=current_user.id
    )


@tasks_group_router.patch(
    "/{tasks_group_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowTasksGroup,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": InvalidCredentialsException},
        status.HTTP_404_NOT_FOUND: {"model": TaskGroupNotFoundException},
        status.HTTP_406_NOT_ACCEPTABLE: {"model": UserNotOwnerException},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationException},
    },
)
async def edit_tasks_group(
    tasks_group_data: UpdateTasksGroup,
    tasks_group: TasksGroup = Depends(valid_owned_tasks),
    tasks_group_service: TasksGroupService = Depends(get_tasks_group_service),
):
    return await tasks_group_service.update_tasks_group(
        tasks_group_id=tasks_group.id, tasks_group_data=tasks_group_data
    )


@tasks_group_router.delete(
    "/{tasks_group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": InvalidCredentialsException},
        status.HTTP_404_NOT_FOUND: {"model": TaskGroupNotFoundException},
        status.HTTP_406_NOT_ACCEPTABLE: {"model": UserNotOwnerException},
    },
)
async def delete_tasks_group(
    tasks_group: TasksGroup = Depends(valid_owned_tasks),
    tasks_group_service: TasksGroupService = Depends(get_tasks_group_service),
):
    return await tasks_group_service.delete_tasks_group(tasks_group_id=tasks_group.id)
