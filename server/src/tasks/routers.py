from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from src.tasks.schemas import ShowTask, CreateTask, UpdateTask
from src.tasks.service import TasksService
from src.tasks.dependencies import tasks_service
from src.tasks_group.models import TasksGroup
from src.tasks_group.dependencies import valid_owned_tasks


tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@tasks_router.get("/{tasks_group_id}", response_model=List[ShowTask])
async def get_tasks(
    tasks_group: TasksGroup = Depends(valid_owned_tasks),
    tasks_service: TasksService = Depends(tasks_service),
):
    return await tasks_service.get_from_group(tasks_group_id=tasks_group.id)


@tasks_router.post("/{tasks_group_id}", response_model=ShowTask)
async def create_task(
    task_data: CreateTask,
    tasks_group: TasksGroup = Depends(valid_owned_tasks),
    tasks_service: TasksService = Depends(tasks_service),
):
    try:
        return await tasks_service.create(
            tasks_group_id=tasks_group.id, task_data=task_datas
        )
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{ex}")


@tasks_router.patch("/{tasks_group_id}/{task_id}", response_model=ShowTask)
async def edit_task(
    task_id: int,
    task_data: UpdateTask,
    tasks_group: TasksGroup = Depends(valid_owned_tasks),
    tasks_service: TasksService = Depends(tasks_service),
):
    try:
        return await tasks_service.update(
            task_id=task_id,
            task_data=task_data,
            tasks_group_id=tasks_group.id,
        )
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{ex}")
