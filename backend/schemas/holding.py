from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional, Literal


class HoldingRequest(BaseModel):
    """
    Holding request model represents a holding request in the system.
    """

    portfolio_id: str
    symbol: str
    quantity: int
    currency: str

    model_config = ConfigDict(extra="forbid")


class HoldingUpdateRequest(BaseModel):
    """
    Holding update request model represents a holding update request in the system.
    """

    portfolio_id: Optional[str] = None
    symbol: Optional[str] = None
    quantity: Optional[int] = None
    currency: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class HoldingResponse(BaseModel):
    """
    Holding model represents a holding in the system.
    """

    holding_id: str
    portfolio_id: str
    symbol: str
    quantity: int
    currency: str

    model_config = ConfigDict(extra="forbid")

