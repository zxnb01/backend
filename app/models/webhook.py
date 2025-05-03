from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base  # Corrected: Import Base from app.database

class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    subscriptions = relationship("Subscription", back_populates="webhook")
