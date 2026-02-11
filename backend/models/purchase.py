from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime
from database import Base
from sqlalchemy import ForeignKey
from models.__init__ import new_id

class PurchaseDB(Base):
    """
    PurchaseDB model represents a purchase in the system.
    """

    __tablename__ = "purchases"

    id = Column(String, primary_key=True, default=new_id)
    client_account_id = Column(String, ForeignKey("accounts.account_id"))
    merchant_account_id = Column(String, ForeignKey("accounts.account_id"))
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    tags = Column(JSON, nullable=False, default=[])

    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "client_account_id": self.client_account_id,
            "merchant_account_id": self.merchant_account_id,
            "amount": self.amount,
            "currency": self.currency,
            "tags": self.tags,
            "timestamp": self.timestamp
        }
