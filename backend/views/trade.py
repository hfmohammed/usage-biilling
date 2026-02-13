from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.deps import get_current_user
from database import get_db
from models.portfolio import PortfolioDB
from models.trade import TradeDB
from models.user import UserDB
from schemas.trade import TradeResponse, TradeRequest, TradeUpdateRequest

router = APIRouter(prefix="/api/v1/trade", tags=["trade"])


def _trade_db_to_response(trade_db: TradeDB) -> TradeResponse:
    """
    Convert a TradeDB model to a TradeResponse model.
    """

    if trade_db is None:
        return None

    return TradeResponse(
        trade_id=trade_db.trade_id,
        portfolio_id=trade_db.portfolio_id,
        symbol=trade_db.symbol,
        quantity=trade_db.quantity,
        price=trade_db.price,
        side=trade_db.side,
        currency=trade_db.currency,
        timestamp=trade_db.timestamp,
        tags=trade_db.tags,
    )

@router.get("/health")
def trade_health_check():
    """
    Trade health check endpoint.
    """
    return {"message": "ok"}


# ========= Trade Management =========
@router.post("/", response_model=TradeResponse, status_code=201)
def create_trade(trade: TradeRequest, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    port = db.query(PortfolioDB).filter(
        PortfolioDB.portfolio_id == trade.portfolio_id,
        PortfolioDB.user_id == current_user.user_id,
    ).first()
    if not port:
        raise HTTPException(status_code=403, detail="Portfolio must belong to you")
    trade_db = TradeDB(
        portfolio_id=trade.portfolio_id,
        symbol=trade.symbol,
        quantity=trade.quantity,
        price=trade.price,
        side=trade.side,
        currency=trade.currency,
        tags=trade.tags
    )
    db.add(trade_db)
    db.commit()
    db.refresh(trade_db)
    return _trade_db_to_response(trade_db)


@router.get("/{trade_id}", response_model=TradeResponse, status_code=200)
def get_trade(trade_id: str, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    trade_db = (
        db.query(TradeDB)
        .join(PortfolioDB, TradeDB.portfolio_id == PortfolioDB.portfolio_id)
        .filter(PortfolioDB.user_id == current_user.user_id, TradeDB.trade_id == trade_id)
        .first()
    )
    if not trade_db:
        raise HTTPException(status_code=404, detail="Trade not found")
    return _trade_db_to_response(trade_db)

@router.put("/{trade_id}", response_model=TradeResponse, status_code=200)
def update_trade(trade_id: str, body: TradeUpdateRequest, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    trade_db = (
        db.query(TradeDB)
        .join(PortfolioDB, TradeDB.portfolio_id == PortfolioDB.portfolio_id)
        .filter(PortfolioDB.user_id == current_user.user_id, TradeDB.trade_id == trade_id)
        .first()
    )
    if not trade_db:
        raise HTTPException(status_code=404, detail="Trade not found")
    if body.portfolio_id:
        port = db.query(PortfolioDB).filter(
            PortfolioDB.portfolio_id == body.portfolio_id,
            PortfolioDB.user_id == current_user.user_id,
        ).first()
        if not port:
            raise HTTPException(status_code=403, detail="Portfolio must belong to you")
        trade_db.portfolio_id = body.portfolio_id
    if body.symbol:
        trade_db.symbol = body.symbol
    if body.quantity:
        trade_db.quantity = body.quantity
    if body.price:
        trade_db.price = body.price
    if body.side:
        trade_db.side = body.side
    if body.currency:
        trade_db.currency = body.currency
    if body.timestamp:
        trade_db.timestamp = body.timestamp
    if body.tags:
        trade_db.tags = body.tags


    db.commit()
    db.refresh(trade_db)

    return _trade_db_to_response(trade_db)


@router.delete("/{trade_id}", status_code=200)
def delete_trade(trade_id: str, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    trade_db = (
        db.query(TradeDB)
        .join(PortfolioDB, TradeDB.portfolio_id == PortfolioDB.portfolio_id)
        .filter(PortfolioDB.user_id == current_user.user_id, TradeDB.trade_id == trade_id)
        .first()
    )
    if not trade_db:
        raise HTTPException(status_code=404, detail="Trade not found")
    db.delete(trade_db)
    db.commit()

    return {"message": "Trade deleted successfully"}

