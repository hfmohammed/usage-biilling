import fastapi

from views.purchase import router as purchase_router

app = fastapi.FastAPI()

app.include_router(purchase_router)

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

