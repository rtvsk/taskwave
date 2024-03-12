from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.auth.service import get_current_user_from_token
from src.tasks.schemas import CreateTask
from src.tasks_group.models import TasksGroup
from src.tasks_group.schemas import ShowTasksGroup, UpdateTasksGroup, DeletedTasksGroup
from src.tasks_group.service import TasksGroupService
from src.tasks_group.dependencies import (
    tasks_group_service,
    valid_owned_tasks,
    valid_tasks_group_id,
)

from src.users.models import Users

tasks_group_router = APIRouter(prefix="/tasks", tags=["Tasks_group"])


@tasks_group_router.get("", response_model=List[ShowTasksGroup])
async def users_tasks_group(
    current_user: Users = Depends(get_current_user_from_token),
    tasks_group_service: TasksGroupService = Depends(tasks_group_service),
):
    return await tasks_group_service.get_from_users(current_user=current_user)


@tasks_group_router.post(
    "", response_model=ShowTasksGroup, status_code=status.HTTP_201_CREATED
)
async def create_tasks_group(
    tasks_data: CreateTask,
    current_user: Users = Depends(get_current_user_from_token),
    tasks_group_service: TasksGroupService = Depends(tasks_group_service),
):
    return await tasks_group_service.create(
        tasks_data=tasks_data,
        current_user=current_user,
    )


@tasks_group_router.patch("/{tasks_group_id}", response_model=ShowTasksGroup)
async def edit_tasks_group(
    tasks_data: UpdateTasksGroup,
    tasks_group: TasksGroup = Depends(valid_tasks_group_id),
    current_user: Users = Depends(get_current_user_from_token),
    tasks_group_service: TasksGroupService = Depends(tasks_group_service),
):
    try:
        return await tasks_group_service.update(
            tasks_id=tasks_group.id,
            tasks_data=tasks_data,
            current_user=current_user,
        )
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{ex}")


@tasks_group_router.delete("/{tasks_group_id}", response_model=DeletedTasksGroup)
async def delete_tasks_group(
    tasks_group: TasksGroup = Depends(valid_tasks_group_id),
    current_user: Users = Depends(get_current_user_from_token),
    tasks_group_service: TasksGroupService = Depends(tasks_group_service),
):
    deleted_tasks_group = await tasks_group_service.delete(
        tasks_id=tasks_group.id,
        current_user=current_user,
    )
    return deleted_tasks_group
