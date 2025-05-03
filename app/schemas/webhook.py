from pydantic import BaseModel
from typing import Any

class WebhookPayload(BaseModel):
    # Define the structure of your webhook payload here if you have a common structure
    # Otherwise, you can use a generic type like Dict[str, Any]
    payload: Any