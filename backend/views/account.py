from fastapi import APIRouter
from schemas.account import AccountRequest, AccountResponse, AccountUpdateRequest
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from models.account import AccountDB

router = APIRouter(prefix="/api/v1/account", tags=["account"])


def _account_db_to_response(account_db: AccountDB) -> AccountResponse:
    """
    Convert a AccountDB model to a AccountResponse model.
    """

    if account_db is None:
        return None

    return AccountResponse(
        account_id=account_db.account_id,
        user_id=account_db.user_id,
        type=account_db.type,
        status=account_db.status,
        currency=account_db.currency,
        created_at=account_db.created_at,
        updated_at=account_db.updated_at
    )


@router .get("/healh")
def account_health_check():
    """
    Account health check endpoint.
    """

    return {"message": "ok"}


#========= Account Management =========
@router.post("/", response_model=AccountResponse, status_code=201)
def create_account(account: AccountRequest, db: Session = Depends(get_db)):
    account_db = AccountDB(
        user_id=account.user_id,
        type=account.type,
        status=account.status,
        currency=account.currency
    )
    db.add(account_db)
    db.commit()
    db.refresh(account_db)

    return _account_db_to_response(account_db)

@router.get("/{account_id}", response_model=AccountResponse, status_code=200)
def get_account(account_id: str, db: Session = Depends(get_db)):
    account_db = db.query(AccountDB).filter(AccountDB.account_id == account_id).first()
    if not account_db:
        raise HTTPException(status_code=404, detail="Account not found")

    return _account_db_to_response(account_db)

@router.put("/{account_id}", response_model=AccountResponse, status_code=200)
def update_account(account_id: str, body: AccountUpdateRequest, db: Session = Depends(get_db)):
    account_db = db.query(AccountDB).filter(AccountDB.account_id == account_id).first()
    if not account_db:
        raise HTTPException(status_code=404, detail="Account not found")

    if body.user_id:
        account_db.user_id = body.user_id
    if body.type:
        account_db.type = body.type
    if body.status:
        account_db.status = body.status
    if body.currency:
        account_db.currency = body.currency

    account_db.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(account_db)

    return _account_db_to_response(account_db)

@router.delete("/{account_id}", status_code=200)
def delete_account(account_id: str, db: Session = Depends(get_db)):
    account_db = db.query(AccountDB).filter(AccountDB.account_id == account_id).first()
    if not account_db:
        raise HTTPException(status_code=404, detail="Account not found")

    db.delete(account_db)
    db.commit()

    return {"message": "Account deleted successfully"}
