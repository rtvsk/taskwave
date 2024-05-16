from datetime import timedelta, datetime, UTC
from jose import jwt

from src.config import settings


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.jwt.SECRET_KEY.get_secret_value(),
        algorithm=settings.jwt.ALGORITHM,
    )
    return encoded_jwt
