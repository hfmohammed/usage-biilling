import fastapi
from schemas.core_models import *
from views.purchase import router as purchase_router
from database import engine, Base
import models.purchase

app = fastapi.FastAPI()


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


app.include_router(purchase_router)

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

#========= User Management =========
@app.post("/api/v1/create_user")
def create_user(user: User):
    pass

@app.get("/api/v1/get_user")
def get_user(user: User):
    pass

@app.post("/api/v1/update_user")
def update_user(user: User):
    pass

@app.delete("/api/v1/delete_user")
def delete_user(user: User):
    pass

#========= Account Management =========
@app.post("/api/v1/create_account")
def create_account(account: Account):
    pass

@app.get("/api/v1/get_account")
def get_account(account: Account):
    pass

@app.post("/api/v1/update_account")
def update_account(account: Account):
    pass

@app.delete("/api/v1/delete_account")
def delete_account(account: Account):
    pass

#========= Transaction Management =========
@app.post("/api/v1/create_transaction")
def create_transaction(transaction: Transaction):
    pass

@app.get("/api/v1/get_transaction")
def get_transaction(transaction: Transaction):
    pass

@app.post("/api/v1/update_transaction")
def update_transaction(transaction: Transaction):
    pass

@app.delete("/api/v1/delete_transaction")
def delete_transaction(transaction: Transaction):
    pass

#========= Portfolio Management =========
@app.post("/api/v1/create_portfolio")
def create_portfolio(portfolio: Portfolio):
    pass

@app.get("/api/v1/get_portfolio")
def get_portfolio(portfolio: Portfolio):
    pass

@app.post("/api/v1/update_portfolio")
def update_portfolio(portfolio: Portfolio):
    pass

@app.delete("/api/v1/delete_portfolio")
def delete_portfolio(portfolio: Portfolio):
    pass

#========= Holding Management =========
@app.post("/api/v1/create_holding")
def create_holding(holding: Holding):
    pass

@app.get("/api/v1/get_holding")
def get_holding(holding: Holding):
    pass

@app.post("/api/v1/update_holding")
def update_holding(holding: Holding):
    pass

@app.delete("/api/v1/delete_holding")
def delete_holding(holding: Holding):
    pass

#========= Trade Management =========
@app.post("/api/v1/create_trade")
def create_trade(trade: Trade):
    pass

@app.get("/api/v1/get_trade")
def get_trade(trade: Trade):
    pass

@app.post("/api/v1/update_trade")
def update_trade(trade: Trade):
    pass

@app.delete("/api/v1/delete_trade")
def delete_trade(trade: Trade):
    pass

