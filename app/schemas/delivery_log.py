from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DeliveryLogBase(BaseModel):
    webhook_id: str
    subscription_id: int
    target_url: str
    attempt: int
    outcome: str
    http_status: Optional[int] = None
    error_details: Optional[str] = None
    timestamp: datetime

class DeliveryLog(DeliveryLogBase):
    id: int

    class Config:
        orm_mode = True