from uuid import UUID
from typing import Optional

from src.util.repository import BaseRepository
from src.tasks.models import Task
from src.tasks.schemas import CreateTask, UpdateTask


class TaskService(BaseRepository):
    """
    Service class for handling Task-related CRUD operations.
    """

    model = Task

    async def create(self, task_data: CreateTask, tasks_group_id: UUID) -> Task:
        """
        Create a new task.
        """
        task_dict = task_data.model_dump()
        task_dict["tasks_group_id"] = tasks_group_id

        task = await self.save(task_dict)

        return task

    async def get(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by id.
        """
        task = await self.get_by_id(task_id)

        return task

    async def get_from_tasks_group(self, tasks_group_id: UUID) -> Optional[list[Task]]:
        """
        Retrieve all tasks belonging to the tasks group.
        """
        tasks = await self.get_by_field("tasks_group_id", tasks_group_id, all=True)

        return tasks

    async def update_task(self, task_data: UpdateTask, task_id: int) -> Task:
        """
        Update a task.
        """
        updated_task_params = task_data.model_dump(exclude_none=True)
        updated_task = await self.update("id", task_id, updated_task_params)

        return updated_task

    async def delete_task(self, task_id: int) -> None:
        """
        Delete a task by id.
        """
        await self.delete(task_id)
