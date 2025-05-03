# from celery import Celery
# import requests
# from datetime import datetime
# from ..core.security import verify_signature
# from .. import models, database

# celery = Celery(__name__, broker="redis://localhost:6379/0")

# @celery.task(bind=True)
# def process_webhook(self, subscription_id, payload):
#     db = database.SessionLocal()
#     subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    
#     if not subscription:
#         return "Subscription not found"
    
#     # Signature verification
#     if subscription.secret:
#         signature = payload.get('signature')
#         verify_signature(payload, signature, subscription_id)
    
#     # Send the request
#     response = requests.post(subscription.target_url, json=payload)
    
#     delivery = models.DeliveryAttempt(
#         subscription_id=subscription.id,
#         target_url=subscription.target_url,
#         timestamp=datetime.utcnow(),
#         attempt_number=1,
#         status="success" if response.status_code == 200 else "failed",
#         http_status=response.status_code
#     )
#     db.add(delivery)
#     db.commit()
#     db.close()
#     return "Webhook processed"
from datetime import timedelta
from sqlalchemy import func
from ..database import get_db
from ..models import DeliveryLog
from ..core.config import LOG_RETENTION_HOURS
from ..worker import celery

@celery.task
def cleanup_delivery_logs():
    db = next(get_db())
    cutoff_date = func.now() - timedelta(hours=LOG_RETENTION_HOURS)
    deleted_count = db.query(DeliveryLog).filter(DeliveryLog.timestamp < cutoff_date).delete()
    db.commit()
    print(f"Cleaned up {deleted_count} old delivery logs.")
    db.close()