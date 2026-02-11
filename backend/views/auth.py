"""
User registration: validate input, hash password, create user.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from database import get_db
from models.user import UserDB

from schemas.auth import SignUpRequest
from auth.password import hash_password
from auth.jwt import create_access_token
from auth.password import verify_password


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/signup")
def signup(body: SignUpRequest, db: Session = Depends(get_db)):
    """
    Register a new user. Email must be unique. Password is stored hashed.
    """
    existing = db.query(UserDB).filter(UserDB.email == body.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = UserDB(
        email=body.email.lower(),
        password_hash=hash_password(body.password),
        name=body.name,
        phone=body.phone or "",
        address=body.address or "",
        city=body.city or "",
        state=body.state or "",
        zip=body.zip or "",
        country=body.country or "",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created", "user_id": user.user_id}


"""
Login: verify email/password, return Bearer JWT.
"""

@router.post("/login", response_model=dict)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Accept form body: username=email, password. Returns access_token for Bearer auth.
    """
    user = db.query(UserDB).filter(UserDB.email == form.username.lower()).first()
    if not user or not getattr(user, "password_hash", None) or not verify_password(form.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token = create_access_token(subject=user.user_id)
    return {"access_token": token, "token_type": "bearer"}

