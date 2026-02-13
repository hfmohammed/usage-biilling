from fastapi import APIRouter
from schemas.user import UserRequest, UserUpdateRequest, UserResponse
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from models.user import UserDB


router = APIRouter(prefix="/api/v1/user", tags=["user"])


def _user_db_to_response(user_db: UserDB) -> UserResponse:
    """
    Convert a UserDB model to a UserResponse model.
    """

    if user_db is None:
        return None

    return UserResponse(
        user_id=user_db.user_id,
        name=user_db.name,
        email=user_db.email,
        phone=user_db.phone,
        address=user_db.address,
        city=user_db.city,
        state=user_db.state,
        zip=user_db.zip,
        country=user_db.country,
        created_at=user_db.created_at,
        updated_at=user_db.updated_at
    )


@router.get("/health")
def user_health_check():
    """
    User health check endpoint.
    """
    return {"message": "ok"}


# ========= User Management =========
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserRequest, db: Session = Depends(get_db)):
    user_db = UserDB(
        name=user.name,
        email=user.email,
        phone=user.phone,
        address=user.address,
        city=user.city,
        state=user.state,
        zip=user.zip if user.zip else None,
        country=user.country
    )

    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return _user_db_to_response(user_db)


@router.get("/{user_id}", response_model=UserResponse, status_code=200)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user_db = db.query(UserDB).filter(UserDB.user_id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    return _user_db_to_response(user_db)


@router.put("/{user_id}", response_model=UserResponse, status_code=200)
def update_user(user_id: str, body: UserUpdateRequest, db: Session = Depends(get_db)):
    user_db = db.query(UserDB).filter(UserDB.user_id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if body.name:
        user_db.name = body.name
    if body.email:
        user_db.email = body.email
    if body.phone:
        user_db.phone = body.phone
    if body.address:
        user_db.address = body.address
    if body.city:
        user_db.city = body.city
    if body.state:
        user_db.state = body.state
    if body.zip:
        user_db.zip = body.zip
    if body.country:
        user_db.country = body.country
    
    user_db.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(user_db)

    return _user_db_to_response(user_db)

@router.delete("/{user_id}", status_code=200)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user_db = db.query(UserDB).filter(UserDB.user_id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user_db)
    db.commit()

    return {"message": "User deleted successfully"}