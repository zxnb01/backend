from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db  # Importing from 'app'
from app.core import cache  # Importing from 'app'
from datetime import datetime

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

# Helper function to fetch subscription from DB or cache
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
    # Use from_orm to map SQLAlchemy model to Pydantic schema
    subscription_schema = schemas.Subscription.from_orm(db_subscription)
    cache.set_cached_subscription(subscription_id, subscription_schema.dict())
    return subscription_schema  # Return schema, not model

# Route to create a new subscription
@router.post("/", response_model=schemas.Subscription, status_code=status.HTTP_201_CREATED)
def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    """
    Creates a new subscription.
    """
    db_subscription = models.Subscription(**subscription.dict(), created_at=datetime.utcnow())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return schemas.Subscription.from_orm(db_subscription)

# Route to retrieve a subscription by its ID
@router.get("/{subscription_id}", response_model=schemas.Subscription)
def read_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a subscription by its ID.
    """
    return get_subscription_from_db_or_cache(subscription_id, db)

# Route to update an existing subscription
@router.put("/{subscription_id}", response_model=schemas.Subscription)
def update_subscription(subscription_id: int, subscription: schemas.SubscriptionUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing subscription.
    """
    db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    
    # Update only the fields that are provided
    for key, value in subscription.dict(exclude_unset=True).items():
        setattr(db_subscription, key, value)
    
    db.commit()
    db.refresh(db_subscription)
    cache.invalidate_cached_subscription(subscription_id)
    return schemas.Subscription.from_orm(db_subscription)

# Route to delete a subscription
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
