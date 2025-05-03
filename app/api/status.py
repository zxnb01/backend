# # Auto-generated
# from fastapi import APIRouter, HTTPException
# from sqlalchemy.orm import Session
# from .. import models, schemas, database

# router = APIRouter()

# @router.get("/{webhook_request_id}")
# def get_delivery_status(webhook_request_id: str, db: Session = database.get_db()):
#     webhook_request = db.query(models.WebhookRequest).filter(models.WebhookRequest.id == webhook_request_id).first()
#     if not webhook_request:
#         raise HTTPException(status_code=404, detail="Webhook request not found")
#     return webhook_request

# @router.get("/subscription/{subscription_id}/recent")
# def get_recent_deliveries(subscription_id: str, db: Session = database.get_db()):
#     deliveries = db.query(models.DeliveryAttempt).filter(models.DeliveryAttempt.subscription_id == subscription_id).order_by(models.DeliveryAttempt.timestamp.desc()).limit(20).all()
#     return deliveries
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import DeliveryLog, Subscription
from ..schemas import DeliveryLog as DeliveryLogSchema
from typing import List

router = APIRouter(prefix="/status", tags=["status"])

@router.get("/{webhook_id}", response_model=List[DeliveryLogSchema])
def get_delivery_status(webhook_id: str, db: Session = Depends(get_db)):
    delivery_logs = db.query(DeliveryLog).filter(DeliveryLog.webhook_id == webhook_id).order_by(DeliveryLog.timestamp.desc()).all()
    return delivery_logs

@router.get("/subscriptions/{subscription_id}/logs", response_model=List[DeliveryLogSchema])
def get_subscription_logs(subscription_id: int, db: Session = Depends(get_db), limit: int = Query(default=20, le=100)):
    db_subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    delivery_logs = db.query(DeliveryLog).filter(DeliveryLog.subscription_id == subscription_id).order_by(DeliveryLog.timestamp.desc()).limit(limit).all()
    return delivery_logs