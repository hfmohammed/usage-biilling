from fastapi import APIRouter
from schemas.transaction import TransactionResponse, TransactionRequest, TransactionUpdateRequest
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from models.transaction import TransactionDB

router = APIRouter(prefix="/api/v1/transaction", tags=["transaction"])


def _transaction_db_to_response(transaction_db: TransactionDB) -> TransactionResponse:
    """
    Convert a TransactionDB model to a TransactionResponse model.
    """

    if transaction_db is None:
        return None

    return TransactionResponse(
        transaction_id=transaction_db.transaction_id,
        account_id=transaction_db.account_id,
        type=transaction_db.type,
        amount=transaction_db.amount,
        currency=transaction_db.currency,
        description=transaction_db.description,
        timestamp=transaction_db.timestamp
    )


@router.get("/health")
def transaction_health_check():
    """
    Transaction health check endpoint.
    """
    return {"message": "ok"}

# ========= Transaction Management =========
@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(transaction: TransactionRequest, db: Session = Depends(get_db)):
    transaction_db = TransactionDB(
        account_id=transaction.account_id,
        type=transaction.type,
        amount=transaction.amount,
        currency=transaction.currency,
        description=transaction.description
    )

    db.add(transaction_db)
    db.commit()
    db.refresh(transaction_db)

    return _transaction_db_to_response(transaction_db)


@router.get("/{transaction_id}", response_model=TransactionResponse, status_code=200)
def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    transaction_db = db.query(TransactionDB).filter(TransactionDB.transaction_id == transaction_id).first()

    if not transaction_db:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return _transaction_db_to_response(transaction_db)


@router.put("/{transaction_id}", response_model=TransactionResponse, status_code=200)
def update_transaction(transaction_id: str, body: TransactionUpdateRequest, db: Session = Depends(get_db)):
    transaction_db = db.query(TransactionDB).filter(TransactionDB.transaction_id == transaction_id).first()

    if not transaction_db:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if body.account_id:
        transaction_db.account_id = body.account_id
    if body.type:
        transaction_db.type = body.type
    if body.amount:
        transaction_db.amount = body.amount
    if body.currency:
        transaction_db.currency = body.currency
    if body.description:
        transaction_db.description = body.description
    if body.timestamp:
        transaction_db.timestamp = body.timestamp

    db.commit()
    db.refresh(transaction_db)

    return _transaction_db_to_response(transaction_db)

@router.delete("/{transaction_id}", status_code=200)
def delete_transaction(transaction_id: str, db: Session = Depends(get_db)):
    transaction_db = db.query(TransactionDB).filter(TransactionDB.transaction_id == transaction_id).first()

    if not transaction_db:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction_db)
    db.commit()

    return {"message": "Transaction deleted successfully"}
