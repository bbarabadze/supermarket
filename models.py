from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4


class Report(BaseModel):
    email: str
    sms: str


class Item(BaseModel):
    item_id: int
    name: str
    price: float
    category: str


class Order(BaseModel):
    report: Report
    timestamp: str
    store_name: str
    user_location: str
    customer_id: int
    items: list[Item]
    total_price: float


class OrderStatus(BaseModel):
    order_id: str
    status: str
    check_status: str