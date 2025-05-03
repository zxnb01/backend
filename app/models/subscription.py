# from sqlalchemy import Column, Integer, String, DateTime
# from app.database import Base

# class Subscription(Base):
#     __tablename__ = 'subscriptions'

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(String(50), index=True)
#     event_type = Column(String(50))
#     status = Column(String(50))
#     created_at = Column(DateTime)
#     updated_at = Column(DateTime)
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base  # Import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    webhook_id = Column(Integer, ForeignKey("webhooks.id"), nullable=False)

    webhook = relationship("Webhook", back_populates="subscriptions")
    delivery_logs = relationship("DeliveryLog", back_populates="subscription")