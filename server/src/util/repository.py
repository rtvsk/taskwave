from uuid import UUID
from typing import Any, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, delete

from src.database import Base
from src.exceptions import BadRequestException, DatabaseException

T = TypeVar("T", bound=Base)


class BaseRepository:
    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, playload: dict[str, Any]) -> T:
        """
        Save data in the database
        """
        try:
            entity = self.model(**playload)
            self.session.add(entity)

            await self.session.commit()
            return entity
        except Exception:
            raise DatabaseException

    async def get_by_id(self, entity_id: UUID | int) -> T | None:
        """
        Retrieve data from the database for the id
        """
        try:
            result = await self.session.execute(
                select(self.model).where(and_(self.model.id == entity_id))
            )
            return result.scalar_one_or_none()
        except Exception:
            raise DatabaseException

    async def get_by_field(
        self, key: str, value: str, all: bool = False
    ) -> T | list[T] | None:
        """
        Retrieve data from the database for the given key with the specified value
        """
        try:
            result = await self.session.execute(
                select(self.model).where(and_(getattr(self.model, key) == value))
            )
            if all:
                entities = result.fetchall()
                return [entity[0] for entity in entities]

            return result.scalar_one_or_none()
        except Exception:
            raise DatabaseException

    async def update(self, key: str, value: Any, playload: dict[str, Any]) -> T | None:
        """
        Update data in the database for the given key with the specified value
        """
        if not playload:
            raise BadRequestException(
                detail="At least one parameter for user update info should be provided"
            )
        try:
            query = (
                update(self.model)
                .where(getattr(self.model, key) == value)
                .values(playload)
                .returning(self.model)
            )
            result = await self.session.execute(query)
            await self.session.commit()

            return result.scalar_one_or_none()
        except Exception:
            raise DatabaseException

    async def delete(self, entity_id: UUID | int) -> None:
        """
        Delete data from the database by the id
        """
        try:
            await self.session.execute(
                delete(self.model).where(self.model.id == entity_id)
            )
            await self.session.commit()
        except Exception:
            raise DatabaseException
