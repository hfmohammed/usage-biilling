from fastapi import APIRouter, HTTPException, Depends
from models.purchase import PurchaseDB
from schemas.purchase import PurchaseResponse, PurchaseRequest
from sqlalchemy.orm import Session
from database import get_db
from typing import List

from events import publish_event


router = APIRouter(prefix="/api/v1/purchase", tags=["purchase"])


def _purchase_db_to_response(purchase_db: PurchaseDB) -> PurchaseResponse:
    """
    Convert a PurchaseDB model to a PurchaseResponse model.
    """

    if purchase_db is None:
        return None

    return PurchaseResponse(
        purchase_id=purchase_db.id,
        client_id=purchase_db.client_id,
        merchant_id=purchase_db.merchant_id,
        amount=purchase_db.amount,
        currency=purchase_db.currency,
        tags=purchase_db.tags,
        timestamp=purchase_db.timestamp,
    )


@router.get("/health")
def purchase_health_check():
    """
    Purchase health check endpoint.
    """
    
    return {"message": "ok"}

@router.get("/list_purchases", response_model=List[PurchaseResponse], status_code=200)
def list_purchases(db: Session = Depends(get_db), limit: int = 20, offset: int = 0):
    purchase_db_list = (
        db.query(PurchaseDB)
        .order_by(PurchaseDB.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [_purchase_db_to_response(p) for p in purchase_db_list]


# ========= Purchase Management =========
@router.post("/", response_model=PurchaseResponse, status_code=201)
def create_purchase(purchase_request: PurchaseRequest, db: Session = Depends(get_db)):
    purchase_db = PurchaseDB(
        client_id=purchase_request.client_id,
        merchant_id=purchase_request.merchant_id,
        amount=purchase_request.amount,
        currency=purchase_request.currency,
        tags=purchase_request.tags
    )

    db.add(purchase_db)
    db.commit()
    db.refresh(purchase_db)

    # Publish event (stub for now; swap for Kafka later)
    publish_event("purchase_recorded", {
        "purchase_id": purchase_db.id,
        "client_id": purchase_db.client_id,
        "merchant_id": purchase_db.merchant_id,
        "amount": purchase_db.amount,
        "currency": purchase_db.currency,
        "tags": purchase_db.tags,
        "timestamp": purchase_db.timestamp.isoformat() if purchase_db.timestamp else None,
    })

    return _purchase_db_to_response(purchase_db)


@router.get("/{purchase_id}", response_model=PurchaseResponse, status_code=200)
def get_purchase(purchase_id: str, db: Session = Depends(get_db)):
    purchase_db = db.query(PurchaseDB).filter(PurchaseDB.id == purchase_id).first()
    if not purchase_db:
        raise HTTPException(status_code=404, detail="Purchase not found")

    return _purchase_db_to_response(purchase_db)


@router.put("/{purchase_id}", response_model=PurchaseResponse, status_code=200)
def update_purchase(purchase_id: str, body: PurchaseUpdateRequest, db: Session = Depends(get_db)):
    purchase_db = db.query(PurchaseDB).filter(PurchaseDB.id == purchase_id).first()
    if not purchase_db:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    if body.client_id:
        purchase_db.client_id = body.client_id
    
    if body.merchant_id:
        purchase_db.merchant_id = body.merchant_id
    
    if body.amount:
        purchase_db.amount = body.amount
    
    if body.currency:
        purchase_db.currency = body.currency
    
    if body.tags:
        purchase_db.tags = body.tags

    db.commit()
    db.refresh(purchase_db)

    return _purchase_db_to_response(purchase_db)


@router.delete("/{purchase_id}", status_code=200)
def delete_purchase(purchase_id: str, db: Session = Depends(get_db)):
    purchase_db = db.query(PurchaseDB).filter(PurchaseDB.id == purchase_id).first()
    if not purchase_db:
        raise HTTPException(status_code=404, detail="Purchase not found")

    db.delete(purchase_db)
    db.commit()

    return {"message": "Purchase deleted successfully"}