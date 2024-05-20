from uuid import UUID

from src.util.repository import BaseRepository
from src.tasks.models import Task
from src.tasks.schemas import CreateTask, UpdateTask
from src.tasks.exceptions import TaskNotFound


class TaskService(BaseRepository):
    model = Task

    async def create(self, task_data: CreateTask, tasks_group_id: UUID) -> Task:
        task_dict = task_data.model_dump()
        task_dict["tasks_group_id"] = tasks_group_id

        task = await self.save(task_dict)

        return task

    async def get(self, task_id: int) -> Task | None:
        task = await self.get_by_id(task_id)

        return task

    async def get_from_tasks_group(self, tasks_group_id: UUID) -> list[Task] | None:
        tasks = await self.get_by_field("tasks_group_id", tasks_group_id, all=True)

        return tasks

    async def update_task(self, task_data: UpdateTask, task_id: int) -> Task:
        updated_task_params = task_data.model_dump(exclude_none=True)
        updated_task = await self.update("id", task_id, updated_task_params)

        return updated_task

    async def delete_task(self, task_id: int) -> None:
        await self.delete(task_id)
