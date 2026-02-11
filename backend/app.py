from views.me import router as me_router
from views.auth import router as auth_router
from auth.deps import get_current_user
import models.trade
import models.holding
import models.portfolio
import models.transaction
import models.account
import models.user
import models.purchase
from database import engine, Base
from views.portfolio import router as portfolio_router
from views.purchase import router as purchase_router
from views.holding import router as holding_router
from views.account import router as account_router
import fastapi
import logging

from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = fastapi.FastAPI(swagger_ui_parameters={"persistAuthorization": True})


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(account_router)
app.include_router(holding_router)
app.include_router(purchase_router)
app.include_router(portfolio_router)
app.include_router(me_router)


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}
