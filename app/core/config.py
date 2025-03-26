from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic import Field, ConfigDict

load_dotenv()


class DbSettings(BaseSettings):
    DB_USER: str = Field(json_schema_extra=({"env": "DB_USER"}))
    DB_PASS: str = Field(json_schema_extra=({"env": "DB_PASS"}))
    DB_NAME: str = Field(json_schema_extra=({"env": "DB_NAME"}))
    DB_HOST: str = Field(json_schema_extra=({"env": "DB_HOST"}))
    DB_PORT: int = Field(json_schema_extra=({"env": "DB_PORT"}))
    db_echo: bool = Field(True, validation_alias="DEBUG")

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


class Run(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000


class RedisConfig(BaseSettings):
    host: str = "redis"
    port: int = 6379
    redis_url: str = f"redis://{host}"


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    run: Run = Run()
    redis: RedisConfig = RedisConfig()

    model_config = ConfigDict(env_file="../../.env")


settings = Settings()
