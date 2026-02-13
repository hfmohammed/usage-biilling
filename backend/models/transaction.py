from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from datetime import datetime
from database import Base
from models.__init__ import new_id

class TransactionDB(Base):
    """
    TransactionDB model represents a transaction in the system.
    """

    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, default=new_id)
    account_id = Column(String, ForeignKey("accounts.account_id"), nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "account_id": self.account_id,
            "type": self.type,
            "amount": self.amount,
            "currency": self.currency,
            "description": self.description,
            "timestamp": self.timestamp
        }

