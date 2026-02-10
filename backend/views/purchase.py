from fastapi import APIRouter, HTTPException, Depends
from models.purchase import PurchaseDB
from schemas.purchase import PurchaseResponse, PurchaseRequest
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(prefix="/api/v1/purchase", tags=["purchase"])


@router.get("/health")
def purchase_health_check():
    return {"message": "ok"}


# ========= Purchase Management =========
@router.post("/")
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

    purchase_response = PurchaseResponse(
        purchase_id=purchase_db.id,
        client_id=purchase_db.client_id,
        merchant_id=purchase_db.merchant_id,
        amount=purchase_db.amount,
        currency=purchase_db.currency,
        tags=purchase_db.tags,
        timestamp=purchase_db.timestamp
    )

    return {"status_code": 201, "message": "Purchase created successfully", "purchase_id": purchase_response}


@router.get("/{purchase_id}")
def get_purchase(purchase_id: str, db: Session = Depends(get_db)):
    purchase_db = db.query(PurchaseDB).filter(PurchaseDB.id == purchase_id).first()
    if not purchase_db:
        raise HTTPException(status_code=404, detail="Purchase not found")

    purchase_response = PurchaseResponse(
        purchase_id=purchase_db.id,
        client_id=purchase_db.client_id,
        merchant_id=purchase_db.merchant_id,
        amount=purchase_db.amount,
        currency=purchase_db.currency,
        tags=purchase_db.tags,
        timestamp=purchase_db.timestamp
    )

    return {"status_code": 200, "message": "Purchase fetched successfully", "purchase": purchase_response}


@router.put("/{purchase_id}")
def update_purchase(purchase_id: str, body: PurchaseRequest, db: Session = Depends(get_db)):
    purchase_db = db.query(PurchaseDB).filter(PurchaseDB.id == purchase_id).first()
    if not purchase_db:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    purchase_db.client_id = body.client_id
    purchase_db.merchant_id = body.merchant_id
    purchase_db.amount = body.amount
    purchase_db.currency = body.currency
    purchase_db.tags = body.tags

    db.commit()
    db.refresh(purchase_db)

    purchase_response = PurchaseResponse(
        purchase_id=purchase_db.id,
        client_id=purchase_db.client_id,
        merchant_id=purchase_db.merchant_id,
        amount=purchase_db.amount,
        currency=purchase_db.currency,
        tags=purchase_db.tags,
        timestamp=purchase_db.timestamp
    )


    return {"status_code": 200, "message": "Purchase updated successfully", "purchase": purchase_response}


@router.delete("/{purchase_id}")
def delete_purchase(purchase_id: str, db: Session = Depends(get_db)):
    purchase_db = db.query(PurchaseDB).filter(PurchaseDB.id == purchase_id).first()
    if not purchase_db:
        raise HTTPException(status_code=404, detail="Purchase not found")

    db.delete(purchase_db)
    db.commit()

    return {"status_code": 200, "message": "Purchase deleted successfully"}
