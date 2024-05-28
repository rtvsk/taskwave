import logging
from datetime import timedelta, datetime, UTC
from jose import jwt

from src.config import settings


logger = logging.getLogger(__name__)


class JwtToken:

    TOKEN_TYPE_FIELD: str = "type"
    ACCESS_TOKEN_TYPE: str = "access"

    @staticmethod
    def _encode(data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        to_encode.update({"exp": expires_delta})
        encoded = jwt.encode(
            claims=to_encode,
            key=settings.jwt.SECRET_KEY.get_secret_value(),
            algorithm=settings.jwt.ALGORITHM,
        )
        return encoded

    @classmethod
    def decode(cls, token: str | bytes) -> dict:
        decoded = jwt.decode(
            token=token,
            key=settings.jwt.SECRET_KEY.get_secret_value(),
            algorithms=settings.jwt.ALGORITHM,
        )
        return decoded

    @classmethod
    def create_access_token(
        cls, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        logger.debug("Creating token...")
        payload = {cls.TOKEN_TYPE_FIELD: cls.ACCESS_TOKEN_TYPE}
        payload.update(data)
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(
                minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        encoded_access_jwt = cls._encode(data=payload, expires_delta=expire)
        logger.debug("Created")
        return encoded_access_jwt


##############THINK THINK THINK#############
#  ADD REFRESH_TOKEN
