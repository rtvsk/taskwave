from uuid import UUID

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks.models import Task
from src.tasks.schemas import CreateTask, UpdateTask


class TasksService:
    model = Task

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, entity_id: UUID):
        result = await self.session.execute(
            select(self.model).where(self.model.id == entity_id)
        )
        entity = result.fetchone()
        if entity is not None:
            return entity

    async def get_from_group(self, tasks_group_id: UUID):
        get_tasks = await self.session.execute(
            select(self.model).where(
                and_(
                    self.model.tasks_group_id == tasks_group_id,
                    self.model.is_active,
                )
            )
        )
        tasks = get_tasks.fetchall()
        return [task[0] for task in tasks]

    async def create(self, tasks_group_id: UUID, task_data: CreateTask):
        task = self.model(
            title=task_data.title,
            description=task_data.description,
            tasks_group_id=tasks_group_id,
        )

        self.session.add(task)
        await self.session.commit()
        return task

    async def update(self, task_id: int, task_data: UpdateTask, tasks_group_id: UUID):
        updated_params = task_data.model_dump(exclude_none=True)
        if not updated_params:
            raise ValueError(
                "At least one parameter for user update info should be provided"
            )

        query = (
            update(self.model)
            .where(
                and_(
                    self.model.id == task_id,
                    self.model.tasks_group_id == tasks_group_id,
                )
            )
            .values(updated_params)
            .returning(
                self.model.id,
                self.model.title,
                self.model.description,
                self.model.is_done,
            )
        )
        res = await self.session.execute(query)
        await self.session.commit()
        updated_task = res.fetchone()
        return updated_task
