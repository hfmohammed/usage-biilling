from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from datetime import datetime
from database import Base
from models.__init__ import new_id

class HoldingDB(Base):
    """
    HoldingDB model represents a holding in the system.
    """

    __tablename__ = "holdings"

    holding_id = Column(String, primary_key=True, default=new_id)
    portfolio_id = Column(String, ForeignKey("portfolios.portfolio_id"), nullable=False)
    symbol = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "holding_id": self.holding_id,
            "portfolio_id": self.portfolio_id,
            "symbol": self.symbol,
            "quantity": self.quantity,
            "currency": self.currency,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
