from typing import Optional
from src.users.service import UserService
from src.users.models import User
from src.exceptions import InvalidCredentials
from src.util.redis_util import cache_data, redis_cache


class UserAuthService(UserService):
    """
    Service class for user authentication.
    """

    @cache_data("user_login", expire_time=600)
    async def get_user_by_login(self, login: str) -> Optional[User]:
        """
        Retrieve a user from database by login.
        """
        user = await self.get_by_field("login", login)
        return user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify if the provided password matches the stored hashed password.
        """
        return self._PWD_CONTEXT.verify(plain_password, hashed_password)

    async def authentificate_user(self, login: str, password: str) -> User:
        """
        Authenticate a user by the provided login and password.

        If the provided login or password is incorrect,
        InvalidCredentials exception is raised.
        """
        user = await self.get_user_by_login(login=login)

        if user and self.verify_password(password, user.hashed_password):
            return user
        else:
            raise InvalidCredentials(detail="Incorrect login or password")

    async def verified_user(self, current_user: User) -> None:
        """
        Update the user's status `is_verified` to `True` in the database.
        """
        await self.update("id", current_user.id, {"is_verified": True})

        redis_cache.delete(f"user_login:{current_user.login}")
