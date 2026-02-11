from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from datetime import datetime
from database import Base
from models.__init__ import new_id

class TradeDB(Base):
    """
    TradeDB model represents a trade in the system.
    """

    __tablename__ = "trades"

    trade_id = Column(String, primary_key=True, default=new_id)
    portfolio_id = Column(String, ForeignKey("portfolios.portfolio_id"), nullable=False)
    symbol = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    side = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    tags = Column(JSON, nullable=False, default=[])

    def to_dict(self):
        return {
            "trade_id": self.trade_id,
            "portfolio_id": self.portfolio_id,
            "symbol": self.symbol,
            "quantity": self.quantity,
            "price": self.price,
            "side": self.side,
            "currency": self.currency,
            "timestamp": self.timestamp,
            "tags": self.tags,
        }

