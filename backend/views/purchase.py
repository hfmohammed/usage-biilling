from fastapi import APIRouter
import models.purchase as purchase_models

router = APIRouter(prefix="/api/v1/purchase", tags=["purchase"])


@router.get("/health")
def purchase_health_check():
    return {"message": "ok"}

@router.post("/")
def create_purchase(purchase: purchase_models.Purchase):
    pass