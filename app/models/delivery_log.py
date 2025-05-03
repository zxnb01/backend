# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from app.database import Base

# class DeliveryLog(Base):
#     __tablename__ = 'delivery_logs'

#     id = Column(Integer, primary_key=True, index=True)
#     webhook_id = Column(Integer, ForeignKey('webhooks.id'))
#     status = Column(String(50))
#     timestamp = Column(DateTime)

#     webhook = relationship("Webhook", back_populates="delivery_logs")
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base

class DeliveryLog(Base):
    __tablename__ = "delivery_logs"

    id = Column(Integer, primary_key=True, index=True)
    webhook_id = Column(String, index=True, nullable=False)  # Identifier for the original webhook
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    target_url = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    attempt = Column(Integer, default=1)
    outcome = Column(String)  # "Success", "Failed Attempt", "Failure"
    http_status = Column(Integer, nullable=True)
    error_details = Column(String, nullable=True)

    subscription = relationship("Subscription", back_populates="deliveries")