from uuid import UUID
from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks_group.models import TasksGroup
from src.auth.service import get_current_user_from_token
from src.users.models import Users
from src.tasks_group.service import TasksGroupService

from src.database import get_async_session


def tasks_group_service(session: AsyncSession = Depends(get_async_session)):
    return TasksGroupService(session=session)


async def valid_tasks_group_id(
    tasks_group_id: UUID,
    tasks_group_service: TasksGroupService = Depends(tasks_group_service),
):
    tasks_group = await tasks_group_service.get_by_id(tasks_group_id)
    if not tasks_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tasks group not found"
        )

    return tasks_group[0]


async def valid_owned_tasks(
    tasks_group: TasksGroup = Depends(valid_tasks_group_id),
    current_user: Users = Depends(get_current_user_from_token),
):
    if tasks_group.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="User not owner"
        )

    return tasks_group
