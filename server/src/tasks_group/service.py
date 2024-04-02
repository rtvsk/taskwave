from uuid import UUID

from src.exceptions import BadRequestException
from src.tasks_group.schemas import CreateTasksGroup, UpdateTasksGroup
from src.database_2.repository import BaseRepository
from src.database_2.models import TasksGroup
from src.database_2.exceptions import UnprocessableError


class TasksGroupService(BaseRepository):
    model = TasksGroup

    async def create(self, tasks_group_data: CreateTasksGroup, author_id: UUID):
        tasks_group_dict = tasks_group_data.model_dump()
        tasks_group_dict["author_id"] = author_id

        tasks_group = await self._save(tasks_group_dict)

        return tasks_group

    async def get_by_id(self, tasks_group_id: UUID):
        tasks_group = await self._get_by_id(tasks_group_id)

        return tasks_group

    async def get_all_from_user(self, author_id: UUID):
        tasks_groups = await self._get_all_by_field("author_id", author_id)

        return tasks_groups

    async def update(self, tasks_group_id: UUID, tasks_group_data: UpdateTasksGroup):
        updated_task_group_params = tasks_group_data.model_dump(exclude_none=True)

        try:
            updated_tasks_group = await self._update(
                "id", tasks_group_id, updated_task_group_params
            )
        except UnprocessableError as e:
            raise BadRequestException(detail=f"{e}")

        return updated_tasks_group

    async def delete(self, tasks_group_id: UUID) -> None:
        await self._delete(tasks_group_id)
