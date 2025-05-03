from pydantic import BaseModel, HttpUrl, conint
from datetime import datetime
from typing import Optional

class SubscriptionBase(BaseModel):
    target_url: HttpUrl

class SubscriptionCreate(SubscriptionBase):
    webhook_id: conint(gt=0)

class Subscription(SubscriptionBase):
    id: int
    created_at: datetime
    webhook_id: int

    class Config:
        from_attributes = True  # Correct for Pydantic v2.x

class SubscriptionUpdate(BaseModel):
    target_url: Optional[HttpUrl] = None
    webhook_id: Optional[conint(gt=0)] = None

    class Config:
        from_attributes = True  # Correct for Pydantic v2.x
