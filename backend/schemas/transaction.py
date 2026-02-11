from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional, Literal


class TransactionRequest(BaseModel):
    """
    Transaction request model represents a transaction request in the system.
    """

    account_id: str
    type: str
    amount: float
    currency: str
    description: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class TransactionUpdateRequest(BaseModel):
    """
    Transaction update request model represents a transaction update request in the system.
    """

    account_id: Optional[str] = None
    type: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    description: Optional[str] = None
    timestamp: Optional[datetime] = None

    model_config = ConfigDict(extra="forbid")


class TransactionResponse(BaseModel):
    """
    Transaction response model represents a transaction response in the system.
    """

    transaction_id: str
    account_id: str
    type: str
    amount: float
    currency: str
    description: Optional[str] = None
    timestamp: datetime

    model_config = ConfigDict(extra="forbid")

