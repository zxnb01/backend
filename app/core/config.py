# # from pydantic_settings import BaseSettings
# # class Settings(BaseSettings):
# #     # Use the Docker service name "postgres" to reference the PostgreSQL container
# #     DATABASE_URL: str = "postgresql://user:password@postgres:5432/webhook_service_db"

# # settings = Settings()
# import os

# DATABASE_URL = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
# CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
# CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
# DELIVERY_TIMEOUT = 10  # seconds
# LOG_RETENTION_HOURS = 72
# MAX_RETRIES = 5
# RETRY_DELAYS = [10, 30, 60, 300, 900]  # seconds

# from pydantic import BaseSettings
# from functools import lru_cache
# import os

# class Settings(BaseSettings):
#     # Database settings
#     db_host: str = os.environ.get("POSTGRES_HOST", "postgres")
#     db_port: int = int(os.environ.get("POSTGRES_PORT", "5432"))
#     db_user: str = os.environ.get("POSTGRES_USER", "user")
#     db_password: str = os.environ.get("POSTGRES_PASSWORD", "password")
#     db_name: str = os.environ.get("POSTGRES_DB", "webhook_service_db")
#     database_url: str = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

#     # Redis settings
#     redis_host: str = os.environ.get("REDIS_HOST", "redis")
#     redis_port: int = int(os.environ.get("REDIS_PORT", "6379"))
#     redis_url: str = f"redis://{redis_host}:{redis_port}"

#     # Celery settings (if needed here, otherwise in worker.py)
#     celery_broker_url: str = f"redis://{redis_host}:{redis_port}"
#     celery_result_backend: str = f"redis://{redis_host}:{redis_port}"

#     # Other settings
#     delivery_timeout: int = 10  # Seconds
#     max_retries: int = 3
#     retry_delays: list[int] = [5, 10, 20]  # Example retry delays in seconds

#     class Config:
#         case_sensitive = True  # Make environment variable names case-sensitive

# @lru_cache()
# def get_settings() -> Settings:
#     return Settings()

# settings = get_settings()
from pydantic_settings import BaseSettings # Change this line
from functools import lru_cache
import os

class Settings(BaseSettings):
    # ... (rest of your settings class)
    db_host: str = os.environ.get("POSTGRES_HOST", "postgres")
    db_port: int = int(os.environ.get("POSTGRES_PORT", "5432"))
    db_user: str = os.environ.get("POSTGRES_USER", "user")
    db_password: str = os.environ.get("POSTGRES_PASSWORD", "password")
    db_name: str = os.environ.get("POSTGRES_DB", "webhook_service_db")
    database_url: str = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    # Redis settings
    redis_host: str = os.environ.get("REDIS_HOST", "redis")
    redis_port: int = int(os.environ.get("REDIS_PORT", "6379"))
    redis_url: str = f"redis://{redis_host}:{redis_port}"

    # Celery settings (if needed here, otherwise in worker.py)
    celery_broker_url: str = f"redis://{redis_host}:{redis_port}"
    celery_result_backend: str = f"redis://{redis_host}:{redis_port}"

    # Other settings
    delivery_timeout: int = 10  # Seconds
    max_retries: int = 3
    retry_delays: list[int] = [5, 10, 20]  # Example retry delays in seconds

    class Config:
        case_sensitive = True  # Make environment variable names case-sensitive

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()