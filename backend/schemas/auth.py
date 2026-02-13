"""
Request/response schemas for auth (signup, login, token).
"""
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SignUpRequest(BaseModel):
    """Body for POST /api/v1/auth/signup. Send JSON with required fields; rest optional."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    name: str = Field(..., min_length=1)
    phone: str = Field(default="")
    address: str = Field(default="")
    city: str = Field(default="")
    state: str = Field(default="")
    zip: str = Field(default="")
    country: str = Field(default="")

    model_config = ConfigDict(extra="ignore")  # ignore extra keys to avoid 422 from clients


class TokenResponse(BaseModel):
    """Response for POST /auth/login."""

    access_token: str
    token_type: str = "bearer"
