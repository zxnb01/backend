# app/worker.py
from celery import Celery
import requests
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models  # Corrected import:  Import from the 'app' package
from app.schemas.delivery_log import DeliveryLogBase  # Corrected import:  Explicit path
from app.database import get_db  # Corrected import: Explicit path
from app.core.config import settings #Corrected import
from datetime import timedelta
import time

celery = Celery('webhook_service', broker=settings.redis_url, backend=settings.redis_url) #corrected

@celery.task(bind=True, max_retries=settings.max_retries) #Corrected
def queue_webhook_delivery(self, webhook_id: str, subscription_id: int, payload: dict):
    db = next(get_db())
    subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if not subscription:
        log_data = DeliveryLogBase(
            webhook_id=webhook_id,
            subscription_id=subscription_id,
            target_url="N/A",
            attempt=self.request.retries + 1,
            outcome="Failure",
            error_details="Subscription not found",
            timestamp=time.time()  # Approximate time
        )
        db_log = models.DeliveryLog(**log_data.dict())
        db.add(db_log)
        db.commit()
        return

    target_url = subscription.target_url
    attempt = self.request.retries + 1

    try:
        response = requests.post(target_url, json=payload, timeout=settings.delivery_timeout) #corrected
        log_data = DeliveryLogBase(
            webhook_id=webhook_id,
            subscription_id=subscription_id,
            target_url=target_url,
            attempt=attempt,
            outcome="Success" if 200 <= response.status_code < 300 else "Failed Attempt",
            http_status=response.status_code,
            timestamp=time.time()  # Approximate time
        )
        db_log = models.DeliveryLog(**log_data.dict())
        db.add(db_log)
        db.commit()

        if not (200 <= response.status_code < 300) and attempt < settings.max_retries: #corrected
            raise self.retry(countdown=settings.retry_delays[self.request.retries]) #corrected

    except requests.exceptions.RequestException as e:
        log_data = DeliveryLogBase(
            webhook_id=webhook_id,
            subscription_id=subscription_id,
            target_url=target_url,
            attempt=attempt,
            outcome="Failed Attempt",
            error_details=str(e),
            timestamp=time.time()  # Approximate time
        )
        db_log = models.DeliveryLog(**log_data.dict())
        db.add(db_log)
        db.commit()
        if attempt < settings.max_retries: #corrected
            raise self.retry(countdown=settings.retry_delays[self.request.retries]) #corrected
    finally:
        db.close()