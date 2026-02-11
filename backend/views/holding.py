from fastapi import APIRouter
from schemas.holding import HoldingRequest, HoldingResponse, HoldingUpdateRequest
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from models.holding import HoldingDB


router = APIRouter(prefix="/api/v1/holding", tags=["holding"])


def _holding_db_to_response(holding_db: HoldingDB) -> HoldingResponse:
    """
    Convert a HoldingDB model to a HoldingResponse model.
    """

    if holding_db is None:
        return None

    return HoldingResponse(
        holding_id=holding_db.holding_id,
        portfolio_id=holding_db.portfolio_id,
        symbol=holding_db.symbol,
        quantity=holding_db.quantity,
        currency=holding_db.currency,
        created_at=holding_db.created_at,
        updated_at=holding_db.updated_at
    )

@router.get("/health")
def holding_health_check():
    """
    Holding health check endpoint.
    """
    return {"message": "ok"}


@router.post("/", response_model=HoldingResponse, status_code=201)
def create_holding(holding: HoldingRequest, db: Session = Depends(get_db)):
    holding_db = HoldingDB(
        portfolio_id=holding.portfolio_id,
        symbol=holding.symbol,
        quantity=holding.quantity,
        currency=holding.currency
    )
    db.add(holding_db)
    db.commit()
    db.refresh(holding_db)
    return _holding_db_to_response(holding_db)


@router.get("/{holding_id}", response_model=HoldingResponse, status_code=200)
def get_holding(holding_id: str, db: Session = Depends(get_db)):
    holding_db = db.query(HoldingDB).filter(HoldingDB.holding_id == holding_id).first()
    if not holding_db:
        raise HTTPException(status_code=404, detail="Holding not found")
    return _holding_db_to_response(holding_db)


@router.put("/{holding_id}", response_model=HoldingResponse, status_code=200)
def update_holding(holding_id: str, body: HoldingUpdateRequest, db: Session = Depends(get_db)):
    holding_db = db.query(HoldingDB).filter(HoldingDB.holding_id == holding_id).first()
    if not holding_db:
        raise HTTPException(status_code=404, detail="Holding not found")
    
    if body.portfolio_id:
        holding_db.portfolio_id = body.portfolio_id
    if body.symbol:
        holding_db.symbol = body.symbol
    if body.quantity:
        holding_db.quantity = body.quantity
    if body.currency:
        holding_db.currency = body.currency

    holding_db.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(holding_db)
    return _holding_db_to_response(holding_db)

@router.delete("/{holding_id}", status_code=200)
def delete_holding(holding_id: str, db: Session = Depends(get_db)):
    holding_db = db.query(HoldingDB).filter(HoldingDB.holding_id == holding_id).first()
    if not holding_db:
        raise HTTPException(status_code=404, detail="Holding not found")

    db.delete(holding_db)
    db.commit()

    return {"message": "Holding deleted successfully"}
