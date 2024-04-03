from uuid import UUID
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.dependencies import get_current_user_from_token
from src.tasks_group.service import TasksGroupService
from src.tasks_group.models import TasksGroup
from src.tasks_group.exceptions import TasksGroupNotFound, UserNotOwner
from src.users.models import User


async def get_tasks_group_service(session: AsyncSession = Depends(get_async_session)):
    return TasksGroupService(session=session)


async def valid_tasks_group_id(
    tasks_group_id: UUID,
    tasks_group_service: TasksGroupService = Depends(get_tasks_group_service),
):
    tasks_group = await tasks_group_service.get_by_id(tasks_group_id)
    if not tasks_group:
        raise TasksGroupNotFound

    return tasks_group


async def valid_owned_tasks(
    current_user: User = Depends(get_current_user_from_token),
    tasks_group: TasksGroup = Depends(valid_tasks_group_id),
):
    if tasks_group.author_id != current_user.id:
        raise UserNotOwner
    return tasks_group