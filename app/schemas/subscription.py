# from pydantic import BaseModel, HttpUrl
# from uuid import UUID
# from typing import Optional

# class SubscriptionCreate(BaseModel):
#     target_url: HttpUrl
#     event_type: str

# class SubscriptionOut(SubscriptionCreate):
#     id: UUID
from pydantic import BaseModel
from datetime import datetime

class SubscriptionBase(BaseModel):
    target_url: str

class SubscriptionCreate(SubscriptionBase):
    webhook_id: int

class Subscription(SubscriptionBase):
    id: int
    created_at: datetime
    webhook_id: int

    class Config:
        orm_mode = True