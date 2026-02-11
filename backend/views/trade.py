from fastapi import APIRouter
from schemas.trade import TradeResponse, TradeRequest, TradeUpdateRequest
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from models.trade import TradeDB

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
def create_trade(trade: TradeRequest, db: Session = Depends(get_db)):
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
def get_trade(trade_id: str, db: Session = Depends(get_db)):
    trade_db = db.query(TradeDB).filter(TradeDB.trade_id == trade_id).first()

    if not trade_db:
        raise HTTPException(status_code=404, detail="Trade not found")

    return _trade_db_to_response(trade_db)

@router.put("/{trade_id}", response_model=TradeResponse, status_code=200)
def update_trade(trade_id: str, body: TradeUpdateRequest, db: Session = Depends(get_db)):
    trade_db = db.query(TradeDB).filter(TradeDB.trade_id == trade_id).first()

    if not trade_db:
        raise HTTPException(status_code=404, detail="Trade not found")

    if body.portfolio_id:
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
def delete_trade(trade_id: str, db: Session = Depends(get_db)):
    trade_db = db.query(TradeDB).filter(TradeDB.trade_id == trade_id).first()

    if not trade_db:
        raise HTTPException(status_code=404, detail="Trade not found")

    db.delete(trade_db)
    db.commit()

    return {"message": "Trade deleted successfully"}

