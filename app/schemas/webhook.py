from pydantic import BaseModel
from typing import Dict, Any

class WebhookPayload(BaseModel):
    payload: Any  # Keep if you still need this

class Webhook(BaseModel):
    event: str
    timestamp: str
    payload: Dict[str, Any]
