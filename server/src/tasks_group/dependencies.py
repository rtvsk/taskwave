from uuid import UUID
from fastapi import Depends

from src.tasks_group.service import TasksGroupService
from src.tasks_group.exceptions import TasksGroupNotFound, UserNotOwner
from src.auth.dependencies import get_current_user_from_token
from src.database_2.models import TasksGroup, User


async def valid_tasks_group_id(tasks_group_id: UUID):
    tasks_group = await TasksGroupService().get_by_id(tasks_group_id)
    if not tasks_group:
        raise TasksGroupNotFound

    return tasks_group


async def valid_owned_tasks(
    tasks_group: TasksGroup = Depends(valid_tasks_group_id),
    current_user: User = Depends(get_current_user_from_token),
):
    if tasks_group.author_id != current_user.id:
        raise UserNotOwner
    return tasks_group
