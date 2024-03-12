from uuid import UUID
from typing import Optional, Any
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session


class BaseService:
    model = None

    def __init__(self) -> None:
        self._session: AsyncSession = get_async_session

    async def get_by_id(self, entity_id: UUID) -> Any:
        result = await self._session.execute(
            select(self.model).where(
                and_(self.model.id == entity_id, self.model.is_active)
            )
        )
        return result.scalar_one_or_none()
