from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional, Literal


class PurchaseRequest(BaseModel):
    """
    Purchase request model represents a purchase request in the system.
    """

    client_id: str
    merchant_id: str
    amount: float = Field(gt=0)
    currency: Literal["USD", "CAD"]
    tags: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class PurchaseResponse(BaseModel):
    """
    Purchase model represents a purchase in the system.
    """

    purchase_id: str
    client_id: str
    merchant_id: str
    amount: float
    currency: str
    tags: List[str]

    timestamp: datetime
    model_config = ConfigDict(extra="forbid")


