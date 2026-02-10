from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
import uuid

def new_id() -> str:
    return str(uuid.uuid4())

class User(BaseModel):
    """
    User model represents a user of the system.
    """

    user_id: str = Field(default_factory=new_id)
    name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip: str
    country: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(extra="forbid")


class Account(BaseModel):
    """
    Account model represents a user's account in the system.
    """

    account_id: str = Field(default_factory=new_id)
    user_id: str
    type: str
    status: str
    currency: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(extra="forbid")


class Transaction(BaseModel):
    """
    Transaction model represents a transaction in the system.
    """

    transaction_id: str = Field(default_factory=new_id)
    account_id: str
    type: str
    amount: float
    currency: str
    description: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(extra="forbid")


class Portfolio(BaseModel):
    """
    Portfolio model represents a portfolio in the system.
    """

    portfolio_id: str = Field(default_factory=new_id)
    user_id: str
    account_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(extra="forbid")


class Holding(BaseModel):
    """
    Holding model represents a holding in the system.
    """

    holding_id: str = Field(default_factory=new_id)
    portfolio_id: str
    symbol: str
    quantity: int
    currency: str

    model_config = ConfigDict(extra="forbid")


class Trade(BaseModel):
    """
    Trade model represents a trade in the system.
    """

    trade_id: str = Field(default_factory=new_id)
    portfolio_id: str
    symbol: str
    quantity: int
    price: float
    side: str
    currency: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")

