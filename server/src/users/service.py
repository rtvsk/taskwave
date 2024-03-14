from uuid import UUID
from typing import Optional
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import pwd_context
from src.users.models import Users
from src.users.schemas import CreateUser, UpdateUser
from src.users.exceptions import UserAlreadyExists, UserNotFound
from src.utils.service import BaseService


class UsersService:
    model = Users

    def __init__(self, session):
        self.session = session

    async def get_by_id(self, entity_id: UUID):
        result = await self.session.execute(
            select(self.model).where(
                and_(self.model.id == entity_id, self.model.is_active)
            )
        )
        return result.scalar_one_or_none()

    async def check_exists_by_field(self, field_name: str, field_value: str) -> bool:
        result = await self.session.execute(
            select(self.model).where(
                and_(
                    getattr(self.model, field_name) == field_value,
                    self.model.is_active,
                )
            )
        )
        entity = result.fetchone()
        return entity is not None

    async def create(self, user_data: CreateUser):
        if await self.check_exists_by_field("login", user_data.login):
            raise UserAlreadyExists("User with this login already exists!")

        if await self.check_exists_by_field("email", user_data.email):
            raise UserAlreadyExists("User with this email already exists!")

        user = self.model(
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            login=user_data.login,
            email=user_data.email,
            hashed_password=pwd_context.hash(user_data.password),
        )

        self.session.add(user)
        await self.session.commit()
        return user

    async def update(self, user_data: UpdateUser, current_user: Users):
        user = await self.get_by_id(entity_id=current_user.id)
        if not user:
            raise UserNotFound("User not found")

        updated_user_params = user_data.model_dump(exclude_none=True)
        if not updated_user_params:
            raise ValueError(
                "At least one parameter for user update info should be provided"
            )

        # if "email" in updated_user_params:
        #     if await self.check_exists_by_field("email", user_data["email"]):
        #         raise UserAlreadyExists("This email is used by another user")

        query = (
            update(self.model)
            .where(self.model.id == current_user.id)
            .values(updated_user_params)
            .returning(
                self.model.id,
                self.model.login,
                self.model.firstname,
                self.model.lastname,
                self.model.email,
            )
        )
        result = await self.session.execute(query)
        await self.session.commit()
        updated_user = result.fetchone()

        if updated_user is not None:
            return updated_user

    async def deactivate(self, current_user: Users):
        user = await self.get_by_id(entity_id=current_user.id)
        if not user:
            raise UserNotFound("User not found")

        query = (
            update(self.model)
            .where(self.model.id == current_user.id)
            .values(is_active=False)
            .returning(self.model.id, self.model.login)
        )

        result = await self.session.execute(query)
        await self.session.commit()
        deactivated_user = result.fetchone()

        if deactivated_user is not None:
            return deactivated_user
