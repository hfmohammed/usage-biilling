"""
Current user endpoint: GET /me (requires Bearer token).
"""
from fastapi import APIRouter, Depends

from auth.deps import get_current_user
from models.user import UserDB

router = APIRouter()


@router.get("/me")
def me(current_user: UserDB = Depends(get_current_user)):
    """Return the currently authenticated user (no password hash)."""
    return current_user.to_dict()
