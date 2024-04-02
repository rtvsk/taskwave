from passlib.context import CryptContext

from src.exceptions import BadRequestException
from src.users.schemas import CreateUser, UpdateUser
from src.users.exceptions import UserAlreadyExists, UserNotFound

from src.database_2.repository import BaseRepository
from src.database_2.models import User
from src.database_2.exceptions import UnprocessableError


class UserService(BaseRepository):

    model = User

    _PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create(self, user_data: CreateUser):
        if await self._get_by_field("login", user_data.login):
            raise UserAlreadyExists(detail="User with this login already exists!")

        if await self._get_by_field("email", user_data.email):
            raise UserAlreadyExists(detail="User with this email already exists!")

        user_dict = user_data.model_dump()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self._PWD_CONTEXT.hash(password)

        user = await self._save(user_dict)

        return user

    async def update(self, user_data: UpdateUser, current_user: User):
        user = await self._get_by_id(entity_id=current_user.id)
        if not user:
            raise UserNotFound

        updated_user_params = user_data.model_dump(exclude_none=True)
        try:
            updated_user = await self._update("id", user.id, updated_user_params)
        except UnprocessableError as e:
            raise BadRequestException(detail=f"{e}")

        return updated_user

    async def deactivate(self, current_user: User):
        user = await self._get_by_id(current_user.id)
        if not user:
            raise UserNotFound

        try:
            deactivated_user = await self._update(
                "id", current_user.id, {"is_active": False}
            )
        except UnprocessableError as e:
            raise BadRequestException(detail=f"{e}")

        return deactivated_user
