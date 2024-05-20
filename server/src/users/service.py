from uuid import UUID
from passlib.context import CryptContext
from sqlalchemy import select, and_

from src.auth.schemas import CreateUser
from src.users.models import User
from src.users.schemas import UpdateUser
from src.users.exceptions import UserAlreadyExists, UserNotFound

from src.util.repository import BaseRepository
from src.util.redis_util import RedisCache


class UserService(BaseRepository):
    model = User

    _PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def _get_by_id(self, user_id: UUID):
        result = await self.session.execute(
            select(self.model).where(
                and_(self.model.id == user_id, self.model.is_active)
            )
        )
        return result.scalar_one_or_none()

    async def _get_by_field(self, key: str, value: str):
        result = await self.session.execute(
            select(self.model).where(
                and_(getattr(self.model, key) == value, self.model.is_active)
            )
        )
        return result.scalar_one_or_none()

    async def create(self, user_data: CreateUser):
        if await self._get_by_field("login", user_data.login):
            raise UserAlreadyExists(detail="User with this login already exists!")

        if await self._get_by_field("email", user_data.email):
            raise UserAlreadyExists(detail="User with this email already exists!")

        user_dict = user_data.model_dump()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self._PWD_CONTEXT.hash(password)

        user = await self.save(user_dict)

        return user

    async def update(self, user_data: UpdateUser, current_user: User):
        user = await self._get_by_id(current_user.id)
        if not user:
            raise UserNotFound

        updated_user_params = user_data.model_dump(exclude_none=True)
        updated_user = await self._update("id", user.id, updated_user_params)

        RedisCache.delete_cache(f"user_login:{current_user.login}")

        return updated_user

    async def deactivate(self, current_user: User):
        user = await self._get_by_id(current_user.id)
        if not user:
            raise UserNotFound

        deactivated_user = await self._update(
            "id", current_user.id, {"is_active": False}
        )

        RedisCache.delete_cache(f"user_login:{current_user.login}")

        return deactivated_user
