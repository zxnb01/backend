from fastapi import FastAPI
from .database import Base, engine
from .api import subscriptions as subscriptions_router
from .api import ingest as ingest_router
from .api import status as status_router
from .worker import celery as celery_app # Changed: Import celery as celery_app
from fastapi.middleware.cors import CORSMiddleware
from celery.schedules import crontab
from datetime import timedelta

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for your UI
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subscriptions_router.router)
app.include_router(ingest_router.router)
app.include_router(status_router.router)

# Configure Celery beat for periodic tasks
celery_app.conf.beat_schedule = {  # Changed: Use celery_app
    'cleanup-logs-every-3-hours': {
        'task': 'app.background_tasks.delivery_worker.cleanup_delivery_logs',  # Corrected task path
        'schedule': timedelta(hours=3),
    },
}
