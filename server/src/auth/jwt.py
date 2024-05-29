import logging
from typing import Union, Optional
from datetime import timedelta, datetime, UTC
from jose import jwt

from src.config import settings


logger = logging.getLogger(__name__)


class JwtToken:
    """
    Utility class for handling JWT operations.
    """

    @staticmethod
    def _encode(data: dict, expires_delta: timedelta) -> str:
        """
        Encode data into a JWT token with an expiration time.
        """
        to_encode = data.copy()
        to_encode.update({"exp": expires_delta})
        encoded = jwt.encode(
            claims=to_encode,
            key=settings.jwt.SECRET_KEY.get_secret_value(),
            algorithm=settings.jwt.ALGORITHM,
        )
        return encoded

    @classmethod
    def decode(cls, token: Union[str, bytes]) -> dict:
        """
        Decode a JWT token.
        """
        decoded = jwt.decode(
            token=token,
            key=settings.jwt.SECRET_KEY.get_secret_value(),
            algorithms=settings.jwt.ALGORITHM,
        )
        return decoded

    @classmethod
    def create_access_token(
        cls, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a new access token.

        If not expiration time delta for the token provided,
        the default expiration from settings will be used.
        """
        logger.debug("Creating token...")
        payload = data.copy()
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
