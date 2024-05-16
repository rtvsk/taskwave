from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class DatabaseSettings(BaseSettings):
    HOST: str
    PORT: str
    NAME: str
    USER: str
    PASSWORD: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", env_prefix="DB_"
    )

    @property
    def URL(self):
        return SecretStr(
            f"postgresql+asyncpg://{self.USER}:{self.PASSWORD.get_secret_value()}@{self.HOST}:{self.PORT}/{self.NAME}"
        )


class JWTSettings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    SECRET_KEY: SecretStr
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="JWT_", extra="ignore"
    )


class SMTPSettings(BaseSettings):

    EMAIL: str
    PASSWORD: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="SMTP_", extra="ignore"
    )


class RedisSettings(BaseSettings):

    HOST: str
    PORT: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="REDIS_", extra="ignore"
    )


# class TestDatabaseSettings(BaseSettings):
#     HOST: str
#     PORT: str
#     NAME: str
#     USER: str
#     PASSWORD: SecretStr

#     model_config = SettingsConfigDict(
#         env_file=".env", env_file_encoding="utf-8", env_prefix="TEST_DB_"
#     )

#     def URL(self):
#         return SecretStr(
#             f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"
#         )


class Settings(BaseSettings):
    smtp: SMTPSettings = SMTPSettings()
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()

from dotenv import load_dotenv
import os


load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")


TEST_DB_HOST = os.environ.get("TEST_DB_HOST")
TEST_DB_PORT = os.environ.get("TEST_DB_PORT")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME")
TEST_DB_USER = os.environ.get("TEST_DB_USER")
TEST_DB_PASSWORD = os.environ.get("TEST_DB_PASSWORD")
TEST_DATABASE_URL = f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
