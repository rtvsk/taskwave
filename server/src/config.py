import logging
from logging.config import dictConfig
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


class ClientSettings(BaseSettings):

    HOST: str
    PORT: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="CLIENT_",
    )

    @property
    def ORIGIN(self):
        return f"http://{self.HOST}:{self.PORT}"


class TestDatabaseSettings(DatabaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="TEST_DB_",
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
    HOST: str
    PORT: int

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="SMTP_", extra="ignore"
    )


class RedisSettings(BaseSettings):

    HOST: str
    PORT: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="REDIS_",
        extra="ignore",
    )


class CelerySettings(BaseSettings):

    BROKER_URL: str
    RESULT_BACKEND: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="CELERY_",
        extra="ignore",
    )


class LoggingSettings(BaseSettings):

    FORMAT: str
    LEVEL: str
    FILE: str
    IGNORED_LOGGERS: list[str] = ["passlib", "asyncio"]
    IGNORED_LOGGERS_LEVEL: str = "ERROR"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="LOG_", extra="ignore"
    )

    def configure_logging(self):
        dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "default": {"format": self.FORMAT, "datefmt": "%Y-%m-%d %H:%M:%S"},
                },
                "handlers": {
                    "file": {
                        "level": self.LEVEL,
                        "formatter": "default",
                        "class": "logging.FileHandler",
                        "filename": self.FILE,
                    },
                },
                "loggers": {
                    "": {
                        "handlers": ["file"],
                        "level": self.LEVEL,
                        "propagate": False,
                    },
                },
            }
        )

        for log in self.IGNORED_LOGGERS:
            self._set_level(log, self.IGNORED_LOGGERS_LEVEL)

    @staticmethod
    def _set_level(logger: str, level: str):
        logging.getLogger(logger).setLevel(level)


class Settings(BaseSettings):
    smtp: SMTPSettings = SMTPSettings()
    db: DatabaseSettings = DatabaseSettings()
    client: ClientSettings = ClientSettings()
    test_db: TestDatabaseSettings = TestDatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    redis: RedisSettings = RedisSettings()
    celery: CelerySettings = CelerySettings()
    log: LoggingSettings = LoggingSettings()


settings = Settings()
