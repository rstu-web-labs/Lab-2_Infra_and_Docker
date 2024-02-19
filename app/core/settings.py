import os

from dotenv import load_dotenv
from pydantic import PositiveInt
from pydantic_settings import BaseSettings


from app.core.constants.base import Environment

load_dotenv()


class RedisSettings(BaseSettings):
    redis_password: str
    redis_host: str
    redis_port: str
    celery_redis_db: str

    @property
    def celery_broker_url(self):
        return f"redis://:{self.redis_password}@{os.getenv('REDIS_HOST')}:{self.redis_port}/{self.celery_redis_db}"

    @property
    def celery_result_backend(self):
        return f"redis://:{self.redis_password}@{os.getenv('REDIS_HOST')}:{self.redis_port}/{self.celery_redis_db}"


class DatabaseSettings(BaseSettings):
    db_postgres_host: str
    db_postgres_port: int = 5432
    db_postgres_name: str
    db_postgres_username: str
    db_postgres_password: str
    db_postgres_timeout: PositiveInt = 5
    db_postgres_driver: str = "asyncpg"

    @property
    def postgres_host_url(self):
        return (
            f"postgresql+{self.db_postgres_driver}://"
            f"{self.db_postgres_username}:{self.db_postgres_password}"
            f"@{self.db_postgres_host}:{self.db_postgres_port}/"
        )

    @property
    def postgres_database_url(self):
        return f"{self.postgres_host_url}{self.db_postgres_name}"


class Settings(DatabaseSettings, RedisSettings):
    app_title: str = "Cadastral service"
    app_description: str = "Service for creating cadastral numbers"
    secret: str = "where is my money lebowski"
    environment: Environment = Environment.LOCAL
    redis_password: str
    redis_host: str
    redis_port: str
    celery_redis_db: str

    @property
    def celery_broker_url(self):
        return f"redis://:{self.redis_password}@{os.getenv('REDIS_HOST')}:{self.redis_port}/{self.celery_redis_db}"

    @property
    def celery_result_backend(self):
        return f"redis://:{self.redis_password}@{os.getenv('REDIS_HOST')}:{self.redis_port}/{self.celery_redis_db}"

    @property
    def is_prod(self):
        return self.environment == Environment.PROD


settings = Settings()
