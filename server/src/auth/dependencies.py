from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import get_async_session
from src.auth.service import UserAuthService
from src.auth.exceptions import InvalidCredentials
from src.users.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


def get_user_auth_service(session: AsyncSession = Depends(get_async_session)):
    return UserAuthService(session=session)


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    user_auth_service: UserAuthService = Depends(get_user_auth_service),
) -> User | None:
    try:
        playload = jwt.decode(
            token=token,
            key=settings.jwt.SECRET_KEY.get_secret_value(),
            algorithms=[settings.jwt.ALGORITHM],
        )
        login: str = playload.get("sub")
        if login is None:
            raise InvalidCredentials
    except JWTError as e:
        raise InvalidCredentials

    user = await user_auth_service.get_user_by_login(login=login)
    if user is None:
        raise InvalidCredentials
    return user
