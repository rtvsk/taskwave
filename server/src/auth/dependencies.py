from jose import JWTError, jwt

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


from src.config import SECRET_KEY, ALGORITHM
from src.auth.service import UserAuthenticationService
from src.auth.exceptions import InvalidCredentials

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
):
    try:
        playload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = playload.get("sub")
        if login is None:
            raise InvalidCredentials
    except JWTError as e:
        raise InvalidCredentials

    user = await UserAuthenticationService().get_user_by_login(login=login)
    if user is None:
        raise InvalidCredentials
    return user
