from uuid import UUID
from typing import Any

# from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy import select, and_, update, delete

from src.database_2.database_2 import async_session_maker
from src.database_2.exceptions import UnprocessableError


class BaseRepository:

    model = None

    # _ERRORS = (IntegrityError, PendingRollbackError)  # THINK ABOUT THIS

    async def _save(self, playload: dict[str, Any]):
        async with async_session_maker() as session:
            entity = self.model(**playload)

            session.add(entity)
            await session.commit()
            return entity

    async def _get_by_id(self, entity_id: UUID | int):
        async with async_session_maker() as session:
            result = await session.execute(
                select(self.model).where(
                    and_(self.model.id == entity_id, self.model.is_active)
                )
            )
            return result.scalar_one_or_none()

    async def _get_by_field(self, key: str, value: str):
        async with async_session_maker() as session:
            result = await session.execute(
                select(self.model).where(
                    and_(getattr(self.model, key) == value, self.model.is_active)
                )
            )
            return result.scalar_one_or_none()

    async def _get_all_by_field(self, key: str, value: str):
        async with async_session_maker() as session:
            result = await session.execute(
                select(self.model).where(
                    and_(getattr(self.model, key) == value, self.model.is_active)
                )
            )
            entities = result.fetchall()
            return [entity[0] for entity in entities]

    async def _update(self, key: str, value: Any, playload: dict[str, Any]):
        if not playload:
            raise UnprocessableError(
                "At least one parameter for user update info should be provided"
            )

        async with async_session_maker() as session:
            query = (
                update(self.model)
                .where(getattr(self.model, key) == value)
                .values(playload)
                .returning(self.model)
            )

            result = await session.execute(query)
            await session.commit()

        return result.scalar_one_or_none()

    async def _delete(self, entity_id: UUID | int) -> None:
        async with async_session_maker() as session:
            await session.execute(delete(self.model).where(self.model.id == entity_id))
            await session.commit()
