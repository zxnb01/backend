# from fastapi import APIRouter, HTTPException
# from sqlalchemy.orm import Session
# from .. import models, schemas, database

# router = APIRouter()

# @router.post("/", response_model=schemas.Subscription)
# def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = database.get_db()):
#     db_subscription = models.Subscription(
#         target_url=subscription.target_url,
#         secret=subscription.secret,
#         event_types=subscription.event_types
#     )
#     db.add(db_subscription)
#     db.commit()
#     db.refresh(db_subscription)
#     return db_subscription

# @router.get("/{subscription_id}", response_model=schemas.Subscription)
# def get_subscription(subscription_id: str, db: Session = database.get_db()):
#     db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
#     if not db_subscription:
#         raise HTTPException(status_code=404, detail="Subscription not found")
#     return db_subscription

# @router.put("/{subscription_id}", response_model=schemas.Subscription)
# def update_subscription(subscription_id: str, subscription: schemas.SubscriptionUpdate, db: Session = database.get_db()):
#     db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
#     if not db_subscription:
#         raise HTTPException(status_code=404, detail="Subscription not found")
    
#     db_subscription.target_url = subscription.target_url or db_subscription.target_url
#     db_subscription.secret = subscription.secret or db_subscription.secret
#     db_subscription.event_types = subscription.event_types or db_subscription.event_types
#     db.commit()
#     db.refresh(db_subscription)
#     return db_subscription

# @router.delete("/{subscription_id}", response_model=schemas.Subscription)
# def delete_subscription(subscription_id: str, db: Session = database.get_db()):
#     db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
#     if not db_subscription:
#         raise HTTPException(status_code=404, detail="Subscription not found")
#     db.delete(db_subscription)
#     db.commit()
#     return db_subscription
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from .. import models, schemas
# from ..database import get_db
# from ..core import cache
# from datetime import datetime
# router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

# def get_subscription_from_db_or_cache(subscription_id: int, db: Session = Depends(get_db)):
#     cached_subscription = cache.get_cached_subscription(subscription_id)
#     if cached_subscription:
#         return schemas.Subscription(**cached_subscription)
#     db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
#     if db_subscription is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
#     cache.set_cached_subscription(subscription_id, schemas.Subscription.from_orm(db_subscription).dict())
#     return db_subscription

# @router.post("/", response_model=schemas.Subscription, status_code=status.HTTP_201_CREATED)
# def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
#     db_subscription = models.Subscription(**subscription.dict())
#     db.add(db_subscription)
#     db.commit()
#     db.refresh(db_subscription)
#     return db_subscription

# @router.get("/{subscription_id}", response_model=schemas.Subscription)
# def read_subscription(subscription_id: int, db: Session = Depends(get_db)):
#     return get_subscription_from_db_or_cache(subscription_id, db)

# @router.put("/{subscription_id}", response_model=schemas.Subscription)
# def update_subscription(subscription_id: int, subscription: schemas.SubscriptionUpdate, db: Session = Depends(get_db)):
#     db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
#     if db_subscription is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
#     for key, value in subscription.dict(exclude_unset=True).items():
#         setattr(db_subscription, key, value)
#     db.commit()
#     db.refresh(db_subscription)
#     cache.invalidate_cached_subscription(subscription_id)
#     return db_subscription

# @router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
#     db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
#     if db_subscription is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
#     db.delete(db_subscription)
#     db.commit()
#     cache.invalidate_cached_subscription(subscription_id)
#     return None

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas  # Corrected: Import from 'app'
from app.database import get_db  # Corrected: Import from 'app'
from app.core import cache  # Corrected: Import from 'app'
from datetime import datetime

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


def get_subscription_from_db_or_cache(subscription_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a subscription from the cache or the database.
    """
    cached_subscription = cache.get_cached_subscription(subscription_id)
    if cached_subscription:
        return schemas.Subscription(**cached_subscription)  # Use the schema directly
    db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    #  Use from_orm
    subscription_schema = schemas.Subscription.from_orm(db_subscription)
    cache.set_cached_subscription(subscription_id, subscription_schema.dict())
    return db_subscription


@router.post("/", response_model=schemas.Subscription, status_code=status.HTTP_201_CREATED)
def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    """
    Creates a new subscription.
    """
    db_subscription = models.Subscription(**subscription.dict(), created_at=datetime.utcnow())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription



@router.get("/{subscription_id}", response_model=schemas.Subscription)
def read_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a subscription by its ID.
    """
    return get_subscription_from_db_or_cache(subscription_id, db)



@router.put("/{subscription_id}", response_model=schemas.Subscription)
def update_subscription(subscription_id: int, subscription: schemas.SubscriptionUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing subscription.
    """
    db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    for key, value in subscription.dict(exclude_unset=True).items():
        setattr(db_subscription, key, value)
    db.commit()
    db.refresh(db_subscription)
    cache.invalidate_cached_subscription(subscription_id)
    return db_subscription



@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """
    Deletes a subscription by its ID.
    """
    db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    db.delete(db_subscription)
    db.commit()
    cache.invalidate_cached_subscription(subscription_id)
    return None
