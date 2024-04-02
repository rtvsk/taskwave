from uuid import UUID

from src.util.repository import BaseRepository
from src.tasks.models import Task
from src.tasks.schemas import CreateTask, UpdateTask
from src.tasks.exceptions import TaskNotFound


class TaskService(BaseRepository):
    model = Task

    async def create(self, task_data: CreateTask, tasks_group_id: UUID):
        task_dict = task_data.model_dump()
        task_dict["tasks_group_id"] = tasks_group_id

        task = await self._save(task_dict)

        return task

    async def get_by_id(self, task_id: int):
        task = await self._get_by_id(task_id)

        return task

    async def get_from_tasks_group(self, tasks_group_id: UUID):
        tasks = await self._get_all_by_field("tasks_group_id", tasks_group_id)

        return tasks

    async def update(self, task_data: UpdateTask, task_id: int):
        task = await self._get_by_id(task_id)
        if not task:
            raise TaskNotFound

        updated_task_params = task_data.model_dump(exclude_none=True)
        updated_task = await self._update("id", task_id, updated_task_params)

        return updated_task

    async def delete(self, task_id: int) -> None:
        task = await self._get_by_id(task_id)
        if not task:
            raise TaskNotFound

        await self._delete(task_id)
