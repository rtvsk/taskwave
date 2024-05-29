import logging
from typing import Optional
from uuid import UUID
from passlib.context import CryptContext
from sqlalchemy import select, and_

from src.auth.schemas import CreateUser
from src.users.models import User
from src.users.schemas import UpdateUser
from src.users.exceptions import UserAlreadyExists, UserNotFound

from src.util.repository import BaseRepository
from src.util.redis_util import RedisCache


logger = logging.getLogger(__name__)


class UserService(BaseRepository):
    """
    Service class for handling User-related CRUD operations.
    """

    model = User

    _PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Retrieve a user by id if user's status `is_active` is `True`.
        """
        result = await self.session.execute(
            select(self.model).where(
                and_(self.model.id == user_id, self.model.is_active)
            )
        )
        return result.scalar_one_or_none()

    async def get_by_field(self, key: str, value: str) -> Optional[User]:
        """
        Retrieve a user by a specific field if user's status `is_active` is `True`.
        """
        result = await self.session.execute(
            select(self.model).where(
                and_(getattr(self.model, key) == value, self.model.is_active)
            )
        )
        return result.scalar_one_or_none()

    async def create(self, user_data: CreateUser) -> User:
        """
        Create a new user.

        If the user with the provided login or email is already in the database,
        UserAlreadyExists exception is raised.
        """
        if await self.get_by_field("login", user_data.login):
            raise UserAlreadyExists(detail="User with this login already exists!")

        if await self.get_by_field("email", user_data.email):
            raise UserAlreadyExists(detail="User with this email already exists!")

        user_dict = user_data.model_dump()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self._PWD_CONTEXT.hash(password)

        logger.debug(f"Prepared data for creating user: {user_dict}")
        user = await self.save(user_dict)

        return user

    async def update_user(self, user_data: UpdateUser, current_user: User) -> User:
        """
        Update a user.

        If user doesn't exist, UserNotFound exception is raised.
        """
        user = await self.get_by_id(current_user.id)
        if not user:
            raise UserNotFound

        updated_user_params = user_data.model_dump(exclude_none=True)
        updated_user = await self.update("id", user.id, updated_user_params)

        RedisCache.delete_cache(f"user_login:{current_user.login}")

        return updated_user

    async def deactivate(self, current_user: User) -> User:
        """
        Deactivate a user.
        Update the user's status `is_active` to `False` in the database.

        If user doesn't exist, UserNotFound exception is raised.
        """
        user = await self.get_by_id(current_user.id)
        if not user:
            raise UserNotFound

        deactivated_user = await self.update(
            "id", current_user.id, {"is_active": False}
        )

        RedisCache.delete_cache(f"user_login:{current_user.login}")

        return deactivated_user
