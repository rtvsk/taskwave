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

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="SMTP_", extra="ignore"
    )


class RedisSettings(BaseSettings):

    HOST: str
    PORT: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="REDIS_", extra="ignore"
    )


class Settings(BaseSettings):
    smtp: SMTPSettings = SMTPSettings()
    db: DatabaseSettings = DatabaseSettings()
    test_db: TestDatabaseSettings = TestDatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
