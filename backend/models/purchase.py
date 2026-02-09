from pydantic import BaseModel
from datetime import datetime
from typing import List


class Customer(BaseModel):
    customer_id: str
    name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip: str
    country: str
    created_at: datetime
    updated_at: datetime


class Merchant(BaseModel):
    merchant_id: str
    name: str
    category: str
    country: str
    city: str
    state: str
    zip: str
    country: str
    created_at: datetime
    updated_at: datetime


class PurchaseEvent(BaseModel):
    purchase_id: str
    customer_id: str
    merchant_id: str
    amount: float
    currency: str
    timestamp: datetime
    description: str
    category: str
    tags: List[str]
