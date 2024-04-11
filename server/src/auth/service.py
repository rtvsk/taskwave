from src.users.service import UserService
from src.util.redis_util import cache_data


class UserAuthenticationService(UserService):

    @cache_data("user_login", expire_time=600)
    async def get_user_by_login(self, login: str):
        user = await self._get_by_field("login", login)
        return user

    def verify_password(self, plain_password, hashed_password):
        return self._PWD_CONTEXT.verify(plain_password, hashed_password)

    async def authentificate_user(self, login: str, password: str):
        user = await self.get_user_by_login(login=login)
        if not user:
            return

        if not self.verify_password(password, user.hashed_password):
            return

        return user
