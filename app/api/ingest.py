# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# import uuid
# import json
# import requests
# from sqlalchemy.orm import Session
# from .. import models, schemas, database
# from ..core.cache import cache
# from ..background_tasks.delivery_worker import process_webhook

# router = APIRouter()

# class WebhookPayload(BaseModel):
#     event_type: str
#     payload: dict

# @router.post("/{subscription_id}")
# async def ingest_webhook(subscription_id: str, payload: WebhookPayload, db: Session = database.get_db()):
#     subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
#     if not subscription:
#         raise HTTPException(status_code=404, detail="Subscription not found")
    
#     # Cache the subscription for faster access
#     cache.set(subscription_id, json.dumps(subscription.dict()), ex=3600)
    
#     # Process the webhook in the background
#     process_webhook.delay(subscription_id, payload.dict())
#     return {"message": "Webhook received", "status": "accepted"}
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Subscription
from ..schemas import WebhookPayload
from ..worker import queue_webhook_delivery
from ..core.security import verify_signature
import uuid

router = APIRouter(prefix="/ingest", tags=["ingest"])

@router.post("/{subscription_id}", status_code=status.HTTP_202_ACCEPTED)
async def ingest_webhook(
    subscription_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    x_hub_signature_256: str | None = Header(default=None),
):
    db_subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")

    if db_subscription.secret:
        payload_bytes = str(payload).encode('utf-8')
        if not verify_signature(payload_bytes, db_subscription.secret, x_hub_signature_256):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

    webhook_id = str(uuid.uuid4())
    queue_webhook_delivery.delay(webhook_id, subscription_id, payload)
    return {"message": "Webhook accepted for processing", "webhook_id": webhook_id}