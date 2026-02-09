from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/purchase", tags=["purchase"])


@router.get("/health")
def purchase_health_check():
    return {"message": "ok"}

