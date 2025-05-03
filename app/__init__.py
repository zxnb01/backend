# from fastapi import FastAPI
# from .api import subscriptions, ingest, status
# from .core import config

# app = FastAPI()

# # Register API routers
# app.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
# app.include_router(ingest.router, prefix="/ingest", tags=["ingestion"])
# app.include_router(status.router, prefix="/status", tags=["status"])

# # Load configuration
# app.config = config.Config()
# webhook_service/app/__init__.py
from .database import Base, engine, get_db