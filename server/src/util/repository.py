from uuid import UUID
import logging
from typing import Any, TypeVar, Optional, Union

from sqlalchemy import select, and_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


from src.database import Base
from src.exceptions import BadRequestException, DatabaseException

T = TypeVar("T", bound=Base)

logger = logging.getLogger(__name__)


class BaseRepository:
    """
    Base repository providing generic database CRUD operations.
    """

    model: type[T] = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, playload: dict[str, Any]) -> T:
        """
        Save a new entity in the database.

        :param payload: data for the new entity.
        :return: the saved entity.
        :raises DatabaseException: if a database error occurs.
        """
        try:
            entity = self.model(**playload)
            self.session.add(entity)

            await self.session.commit()
            return entity
        except SQLAlchemyError as e:
            logger.error(f"Error save data in the database: {e}")
            raise DatabaseException

    async def get_by_id(self, entity_id: Union[UUID, int]) -> Optional[T]:
        """
        Retrieve an entity by id.

        :param entity_id: the id of the entity.
        :return: entity if found, else None.
        :raises DatabaseException: if a database error occurs.
        """
        try:
            result = await self.session.execute(
                select(self.model).where(and_(self.model.id == entity_id))
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Error extracting from the database: {e}")
            raise DatabaseException

    async def get_by_field(
        self, key: str, value: str, all: bool = False
    ) -> Union[T, list[T]]:
        """
        Retrieve entities by a specified field.

        :param key: field name.
        :param value: field value.
        :param all: whether to retrieve all matching entities. Defaults to `False`
        :return: a list of entities if `all` is True, else a single entity or None.
        :raises DatabaseException: if a database error occurs.
        """
        try:
            result = await self.session.execute(
                select(self.model).where(and_(getattr(self.model, key) == value))
            )
            if all:
                entities = result.fetchall()
                return [entity[0] for entity in entities]

            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Error extracting from the database: {e}")
            raise DatabaseException

    async def update(
        self, key: str, value: Any, playload: dict[str, Any]
    ) -> Optional[T]:
        """
        Update an entity in the database.

        :param key: field name to search for the entity.
        :param value: field value to search for the entity.
        :param payload: data for updating the entity.
        :return: The updated entity if found, else None.
        :raises BadRequestException: If no update parameters are provided.
        :raises DatabaseException: If a database error occurs.
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
        except SQLAlchemyError as e:
            logger.error(f"Error updating data in the database: {e}")
            raise DatabaseException

    async def delete(self, entity_id: Union[UUID, int]) -> None:
        """
        Delete an entity from the database by id.

        :param entity_id: the id of the entity.
        :raises DatabaseException: if a database error occurs.
        """
        try:
            await self.session.execute(
                delete(self.model).where(self.model.id == entity_id)
            )
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error deleting in the database: {e}")
            raise DatabaseException
