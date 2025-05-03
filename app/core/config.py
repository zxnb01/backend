# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
import os
class Settings(BaseSettings):
    # Database pieces
    db_host: str = "postgres"
    db_port: int = 5432
    db_user: str = "user"
    db_password: str = "password"
    db_name: str = "webhook_service_db"
    database_url: str = ""             # give default so it's not required

    # Redis pieces
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_url: str = ""                # default

    # Celery pieces
    celery_broker_url: str = ""        # default
    celery_result_backend: str = ""    # default

    # Other settings
    delivery_timeout: int = 10         # seconds
    max_retries: int = 3
    retry_delays: list[int] = [5, 10, 20]

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Now that all db_*, redis_*, etc. are initialized, build the URLs
        self.database_url = (
            f"postgresql://{self.db_user}:"
            f"{self.db_password}@{self.db_host}:"
            f"{self.db_port}/{self.db_name}"
        )
        self.redis_url = f"redis://{self.redis_host}:{self.redis_port}"
        # Often broker/backend are the same as redis_url
        self.celery_broker_url = self.redis_url
        self.celery_result_backend = self.redis_url

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
