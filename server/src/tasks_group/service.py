from uuid import UUID

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks_group.models import TasksGroup
from src.tasks_group.schemas import ShowTasksGroup, UpdateTasksGroup
from src.tasks.schemas import CreateTask
from src.users.models import Users


class TasksGroupService:
    model = TasksGroup

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, entity_id: UUID):
        result = await self.session.execute(
            select(self.model).where(
                and_(self.model.id == entity_id, self.model.is_active)
            )
        )
        entity = result.fetchone()
        if entity is not None:
            return entity

    async def get_from_users(self, current_user: Users):
        get_tasks_group = await self.session.execute(
            select(self.model).where(
                and_(
                    self.model.author_id == current_user.id,
                    self.model.is_active,
                )
            )
        )
        tasks_group = get_tasks_group.fetchall()
        return [group[0] for group in tasks_group]

    async def create(
        self,
        tasks_data: CreateTask,
        current_user: Users,
    ):
        tasks_group = self.model(
            title=tasks_data.title,
            description=tasks_data.description,
            author_id=current_user.id,
        )

        self.session.add(tasks_group)
        await self.session.commit()
        return tasks_group

    async def update(
        self,
        tasks_id: UUID,
        tasks_data: UpdateTasksGroup,
        current_user: Users,
    ):
        updated_params = tasks_data.model_dump(exclude_none=True)
        if not updated_params:
            raise ValueError(
                "At least one parameter for tasks group update info should be provided"
            )

        query = (
            update(self.model)
            .where(
                and_(
                    self.model.id == tasks_id,
                    self.model.author_id == current_user.id,
                )
            )
            .values(updated_params)
            .returning(self.model.id, self.model.title, self.model.description)
        )
        res = await self.session.execute(query)
        await self.session.commit()
        updated_tasks_group = res.fetchone()
        return updated_tasks_group

    async def delete(
        self,
        tasks_id: UUID,
        current_user: Users,
    ):
        query = (
            update(self.model)
            .where(
                and_(
                    self.model.id == tasks_id,
                    self.model.author_id == current_user.id,
                )
            )
            .values(is_active=False)
            .returning(self.model.id, self.model.title, self.model.description)
        )
        res = await self.session.execute(query)
        await self.session.commit()
        deleted_tasks_group = res.fetchone()
        return deleted_tasks_group
