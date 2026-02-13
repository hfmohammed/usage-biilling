from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional


class UserRequest(BaseModel):
    """
    User update request model represents a user update request in the system.
    """

    name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip: Optional[str] = None
    country: str

    model_config = ConfigDict(extra="forbid")


class UserUpdateRequest(BaseModel):
    """
    User update request model represents a user update request in the system.
    """

    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class UserResponse(BaseModel):
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


