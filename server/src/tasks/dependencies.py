from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks.service import TaskService
from src.tasks.exceptions import TaskNotFound
from src.tasks.models import Task
from src.tasks_group.models import TasksGroup
from src.tasks_group.dependencies import valid_owned_tasks
from src.database import get_async_session


def get_task_service(session: AsyncSession = Depends(get_async_session)):
    """
    Provide a TaskService instance.
    """
    return TaskService(session=session)


async def valid_task_id(
    task_id: int, task_service: TaskService = Depends(get_task_service)
) -> Task:
    """
    Validate if a task with the given id exists.

    If task doesn't exist, TaskNotFound error is raised.
    """
    task = await task_service.get(task_id)
    if not task:
        raise TaskNotFound

    return task


async def valid_tasks_group(
    tasks_group: TasksGroup = Depends(valid_owned_tasks),
    task: Task = Depends(valid_task_id),
):
    """
    Validate if a task belongs to a given tasks group.

    If task doesn't belongs for the given tasks group,
    TaskNotFound error is raised.
    """
    if task.tasks_group_id != tasks_group.id:
        raise TaskNotFound
    return task
