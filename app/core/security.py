# import hmac
# import hashlib
# from fastapi import HTTPException
# from .. import config

# def verify_signature(payload: dict, signature: str, subscription_id: str):
#     secret_key = config.Config().secret_key
#     expected_signature = hmac.new(secret_key.encode(), str(payload).encode(), hashlib.sha256).hexdigest()
    
#     if not hmac.compare_digest(expected_signature, signature):
#         raise HTTPException(status_code=400, detail="Invalid signature")
import hashlib
import hmac
from .config import DELIVERY_TIMEOUT  # Import if needed here

def verify_signature(payload_body: bytes, secret_token: str | None, signature_header: str | None) -> bool:
    if not secret_token or not signature_header:
        return True  # No secret or header, skip verification

    try:
        hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
        expected_signature = f"sha256={hash_object.hexdigest()}"
        return hmac.compare_digest(expected_signature, signature_header)
    except Exception as e:
        print(f"Error verifying signature: {e}")
        return False