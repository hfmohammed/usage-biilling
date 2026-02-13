from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from datetime import datetime
from database import Base
from models.__init__ import new_id

class PortfolioDB(Base):
    """
    PortfolioDB model represents a portfolio in the system.
    """

    __tablename__ = "portfolios"

    portfolio_id = Column(String, primary_key=True, default=new_id)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    account_id = Column(String, ForeignKey("accounts.account_id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "portfolio_id": self.portfolio_id,
            "user_id": self.user_id,
            "account_id": self.account_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

