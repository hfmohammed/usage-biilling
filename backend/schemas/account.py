from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional, Literal


class AccountRequest(BaseModel):
    """
    Account model represents a user's account in the system.
    """

    name: str
    type: str
    status: str
    currency: str

    model_config = ConfigDict(extra="forbid")


class AccountResponse(BaseModel):
    """
    AccountResponse model represents a user's account in the system.
    """

    account_id: str
    user_id: str
    name: str
    type: str
    status: str
    currency: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(extra="forbid")


class AccountUpdateRequest(BaseModel):
    """
    AccountUpdateRequest model represents a user's account update request in the system.
    """

    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    currency: Optional[str] = None

    model_config = ConfigDict(extra="forbid")
