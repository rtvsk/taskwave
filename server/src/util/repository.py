from uuid import UUID
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, delete

from src.exceptions import BadRequestException


class BaseRepository:
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _save(self, playload: dict[str, Any]):
        entity = self.model(**playload)
        self.session.add(entity)

        await self.session.commit()
        return entity

    async def _get_by_id(self, entity_id: UUID | int):
        result = await self.session.execute(
            select(self.model).where(and_(self.model.id == entity_id))
        )
        return result.scalar_one_or_none()

    async def _get_by_field(self, key: str, value: str):
        result = await self.session.execute(
            select(self.model).where(and_(getattr(self.model, key) == value))
        )
        return result.scalar_one_or_none()

    async def _get_all_by_field(self, key: str, value: str):
        result = await self.session.execute(
            select(self.model).where(and_(getattr(self.model, key) == value))
        )
        entities = result.fetchall()
        return [entity[0] for entity in entities]

    async def _update(self, key: str, value: Any, playload: dict[str, Any]):
        if not playload:
            raise BadRequestException(
                detail="At least one parameter for user update info should be provided"
            )

        query = (
            update(self.model)
            .where(getattr(self.model, key) == value)
            .values(playload)
            .returning(self.model)
        )
        result = await self.session.execute(query)
        await self.session.commit()

        return result.scalar_one_or_none()

    async def _delete(self, entity_id: UUID | int) -> None:
        await self.session.execute(delete(self.model).where(self.model.id == entity_id))
        await self.session.commit()
