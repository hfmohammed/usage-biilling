from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime
from database import Base
import uuid

def new_id() -> str:
    return str(uuid.uuid4())


class PurchaseDB(Base):
    __tablename__ = "purchases"

    id = Column(String, primary_key=True, default=new_id)
    client_id = Column(String, nullable=False)
    merchant_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    tags = Column(JSON, nullable=False, default=[])

    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "merchant_id": self.merchant_id,
            "amount": self.amount,
            "currency": self.currency,
            "tags": self.tags,
            "timestamp": self.timestamp
        }
