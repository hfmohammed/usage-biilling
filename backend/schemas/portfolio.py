from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional, Literal

class PortfolioRequest(BaseModel):
    """
    Portfolio request model represents a portfolio request in the system.
    """

    user_id: str
    account_id: str

    model_config = ConfigDict(extra="forbid")

class PortfolioResponse(BaseModel):
    """
    Portfolio response model represents a portfolio response in the system.
    """

    portfolio_id: str
    user_id: str
    account_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(extra="forbid")


class PortfolioUpdateRequest(BaseModel):
    """
    Portfolio update request model represents a portfolio update request in the system.
    """

    user_id: Optional[str] = None
    account_id: Optional[str] = None

    model_config = ConfigDict(extra="forbid")