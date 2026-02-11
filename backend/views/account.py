from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.deps import get_current_user
from database import get_db
from models.account import AccountDB
from models.user import UserDB
from schemas.account import AccountRequest, AccountResponse, AccountUpdateRequest
from typing import List

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
        name=account_db.name,
        type=account_db.type,
        status=account_db.status,
        currency=account_db.currency,
        created_at=account_db.created_at,
        updated_at=account_db.updated_at
    )


@router.get("/health")
def account_health_check():
    """
    Account health check endpoint.
    """

    return {"message": "ok"}


# ========= Account queries =========
@router.get("/list_accounts", response_model=List[AccountResponse], status_code=200)
def list_accounts(db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    accounts_db = db.query(AccountDB).filter(
        AccountDB.user_id == current_user.user_id).all()

    return [_account_db_to_response(account_db) for account_db in accounts_db]

# ========= Account Management =========


@router.post("/", response_model=AccountResponse, status_code=201)
def create_account(account: AccountRequest, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):

    if db.query(AccountDB).filter(AccountDB.user_id == current_user.user_id, AccountDB.name == account.name).first():
        raise HTTPException(
            status_code=400, detail="Account name already exists")

    account_db = AccountDB(
        user_id=current_user.user_id,
        name=account.name,
        type=account.type,
        status=account.status,
        currency=account.currency
    )

    db.add(account_db)
    db.commit()
    db.refresh(account_db)

    return _account_db_to_response(account_db)


@router.get("/{account_id}", response_model=AccountResponse, status_code=200)
def get_account(account_id: str, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    account_db = db.query(AccountDB).filter(
        AccountDB.account_id == account_id, AccountDB.user_id == current_user.user_id).first()

    if not account_db:
        raise HTTPException(status_code=404, detail="Account not found")

    return _account_db_to_response(account_db)


@router.put("/{account_id}", response_model=AccountResponse, status_code=200)
def update_account(account_id: str, body: AccountUpdateRequest, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    account_db = db.query(AccountDB).filter(
        AccountDB.account_id == account_id, AccountDB.user_id == current_user.user_id).first()

    if not account_db:
        raise HTTPException(status_code=404, detail="Account not found")

    if body.name:
        account_db.name = body.name
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
def delete_account(account_id: str, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    account_db = db.query(AccountDB).filter(
        AccountDB.account_id == account_id, AccountDB.user_id == current_user.user_id).first()
    if not account_db:
        raise HTTPException(status_code=404, detail="Account not found")

    db.delete(account_db)
    db.commit()

    return {"message": "Account deleted successfully"}
