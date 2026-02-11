from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional, Literal


class PurchaseRequest(BaseModel):
    """
    Purchase request model represents a purchase request in the system.
    """

    client_account_id: str
    merchant_account_id: str
    amount: float = Field(gt=0)
    currency: Literal["USD", "CAD"]
    tags: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class PurchaseResponse(BaseModel):
    """
    Purchase model represents a purchase in the system.
    """

    purchase_id: str
    client_account_id: str
    merchant_account_id: str
    amount: float
    currency: str
    tags: List[str]

    timestamp: datetime
    model_config = ConfigDict(extra="forbid")


class PurchaseUpdateRequest(BaseModel):
    """
    Purchase update request model represents a purchase update request in the system.
    """

    client_account_id: Optional[str] = None
    merchant_account_id: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    tags: Optional[List[str]] = None

    model_config = ConfigDict(extra="forbid")