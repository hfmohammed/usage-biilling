from fastapi import APIRouter
from schemas.portfolio import PortfolioRequest, PortfolioResponse, PortfolioUpdateRequest
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from models.portfolio import PortfolioDB

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
def create_portfolio(portfolio: PortfolioRequest, db: Session = Depends(get_db)):
    portfolio_db = PortfolioDB(
        user_id=portfolio.user_id,
        account_id=portfolio.account_id)

    db.add(portfolio_db)
    db.commit()
    db.refresh(portfolio_db)

    return _portfolio_db_to_response(portfolio_db)


@router.get("/{portfolio_id}", response_model=PortfolioResponse, status_code=200)
def get_portfolio(portfolio_id: str, db: Session = Depends(get_db)):
    portfolio_db = db.query(PortfolioDB).filter(PortfolioDB.portfolio_id == portfolio_id).first()

    if not portfolio_db:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return _portfolio_db_to_response(portfolio_db)

@router.put("/{portfolio_id}", response_model=PortfolioResponse, status_code=200)
def update_portfolio(portfolio_id: str, body: PortfolioUpdateRequest, db: Session = Depends(get_db)):
    portfolio_db = db.query(PortfolioDB).filter(PortfolioDB.portfolio_id == portfolio_id).first()

    if not portfolio_db:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    if body.user_id:
        portfolio_db.user_id = body.user_id

    if body.account_id:
        portfolio_db.account_id = body.account_id

    portfolio_db.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(portfolio_db)

    return _portfolio_db_to_response(portfolio_db)

@router.delete("/{portfolio_id}", status_code=200)
def delete_portfolio(portfolio_id: str, db: Session = Depends(get_db)):
    portfolio_db = db.query(PortfolioDB).filter(PortfolioDB.portfolio_id == portfolio_id).first()

    if not portfolio_db:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    db.delete(portfolio_db)
    db.commit()

    return {"message": "Portfolio deleted successfully"}
