from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.deps import get_current_user
from database import get_db
from models.account import AccountDB
from models.portfolio import PortfolioDB
from models.user import UserDB
from schemas.portfolio import PortfolioRequest, PortfolioResponse, PortfolioUpdateRequest

router = APIRouter(prefix="/api/v1/portfolio", tags=["portfolio"])


def _portfolio_db_to_response(portfolio_db: PortfolioDB) -> PortfolioResponse:
    """
    Convert a PortfolioDB model to a PortfolioResponse model.
    """

    if portfolio_db is None:
        return None

    return PortfolioResponse(
        portfolio_id=portfolio_db.portfolio_id,
        user_id=portfolio_db.user_id,
        account_id=portfolio_db.account_id,
        created_at=portfolio_db.created_at,
        updated_at=portfolio_db.updated_at
    )


@router.get("/health")
def portfolio_health_check():
    """
    Portfolio health check endpoint.
    """
    return {"message": "ok"}

#========= Portfolio Management =========
@router.post("/", response_model=PortfolioResponse, status_code=201)
def create_portfolio(portfolio: PortfolioRequest, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    # Ensure account belongs to current user
    acc = db.query(AccountDB).filter(AccountDB.account_id == portfolio.account_id, AccountDB.user_id == current_user.user_id).first()
    if not acc:
        raise HTTPException(status_code=403, detail="Account must belong to you")
    portfolio_db = PortfolioDB(
        user_id=current_user.user_id,
        account_id=portfolio.account_id)

    db.add(portfolio_db)
    db.commit()
    db.refresh(portfolio_db)

    return _portfolio_db_to_response(portfolio_db)


@router.get("/{portfolio_id}", response_model=PortfolioResponse, status_code=200)
def get_portfolio(portfolio_id: str, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    portfolio_db = db.query(PortfolioDB).filter(
        PortfolioDB.portfolio_id == portfolio_id,
        PortfolioDB.user_id == current_user.user_id,
    ).first()
    if not portfolio_db:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return _portfolio_db_to_response(portfolio_db)

@router.put("/{portfolio_id}", response_model=PortfolioResponse, status_code=200)
def update_portfolio(portfolio_id: str, body: PortfolioUpdateRequest, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    portfolio_db = db.query(PortfolioDB).filter(
        PortfolioDB.portfolio_id == portfolio_id,
        PortfolioDB.user_id == current_user.user_id,
    ).first()
    if not portfolio_db:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    if body.account_id:
        acc = db.query(AccountDB).filter(AccountDB.account_id == body.account_id, AccountDB.user_id == current_user.user_id).first()
        if not acc:
            raise HTTPException(status_code=403, detail="Account must belong to you")
        portfolio_db.account_id = body.account_id
    portfolio_db.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(portfolio_db)

    return _portfolio_db_to_response(portfolio_db)

@router.delete("/{portfolio_id}", status_code=200)
def delete_portfolio(portfolio_id: str, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    portfolio_db = db.query(PortfolioDB).filter(
        PortfolioDB.portfolio_id == portfolio_id,
        PortfolioDB.user_id == current_user.user_id,
    ).first()
    if not portfolio_db:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    db.delete(portfolio_db)
    db.commit()

    return {"message": "Portfolio deleted successfully"}
