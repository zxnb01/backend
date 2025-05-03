from celery import Celery
from os import environ

redis_url = environ.get("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery('webhook_tasks', broker=redis_url, backend='redis')