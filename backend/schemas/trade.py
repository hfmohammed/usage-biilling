from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional, Literal
from schemas.main import new_id


class TradeRequest(BaseModel):
    """
    Trade request model represents a trade request in the system.
    """

    portfolio_id: ForeignKey("portfolios.portfolio_id")
    symbol: str
    quantity: int
    price: float
    side: str
    currency: str
    tags: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class TradeResponse(BaseModel):
    """
    Trade model represents a trade in the system.
    """

    trade_id: str
    portfolio_id: str
    symbol: str
    quantity: int
    price: float
    side: str
    currency: str
    timestamp: datetime
    tags: List[str]

    model_config = ConfigDict(extra="forbid")


class TradeUpdateRequest(BaseModel):
    """
    Trade update request model represents a trade update request in the system.
    """

    portfolio_id: Optional[ForeignKey("portfolios.portfolio_id")] = None
    symbol: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    side: Optional[str] = None
    currency: Optional[str] = None
    tags: Optional[List[str]] = None

    model_config = ConfigDict(extra="forbid")

