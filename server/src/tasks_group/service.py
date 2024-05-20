from uuid import UUID

from typing import Optional

from src.util.repository import BaseRepository
from src.tasks_group.schemas import CreateTasksGroup, UpdateTasksGroup
from src.tasks_group.models import TasksGroup


class TasksGroupService(BaseRepository):
    model = TasksGroup

    async def create(
        self, tasks_group_data: CreateTasksGroup, author_id: UUID
    ) -> TasksGroup:
        tasks_group_dict = tasks_group_data.model_dump()
        tasks_group_dict["author_id"] = author_id

        tasks_group = await self.save(tasks_group_dict)

        return tasks_group

    async def get(self, tasks_group_id: UUID) -> Optional[TasksGroup]:
        tasks_group = await self.get_by_id(tasks_group_id)

        return tasks_group

    async def get_all_from_user(self, author_id: UUID) -> Optional[list[TasksGroup]]:
        tasks_groups = await self.get_by_field("author_id", author_id, all=True)

        return tasks_groups

    async def update_tasks_group(
        self, tasks_group_id: UUID, tasks_group_data: UpdateTasksGroup
    ) -> TasksGroup:
        updated_task_group_params = tasks_group_data.model_dump(exclude_none=True)

        updated_tasks_group = await self.update(
            "id", tasks_group_id, updated_task_group_params
        )

        return updated_tasks_group

    async def delete_tasks_group(self, tasks_group_id: UUID) -> None:
        await self.delete(tasks_group_id)
