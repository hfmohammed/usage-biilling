import logging

import fastapi
from views.account import router as account_router
from views.holding import router as holding_router
from views.purchase import router as purchase_router
from views.portfolio import router as portfolio_router

from database import engine, Base
import models.purchase
import models.user
import models.account
import models.transaction
import models.portfolio
import models.holding
import models.trade

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = fastapi.FastAPI()


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


app.include_router(account_router)
app.include_router(holding_router)
app.include_router(purchase_router)
app.include_router(portfolio_router)

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

