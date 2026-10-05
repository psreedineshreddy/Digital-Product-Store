from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price: float
    subtotal: float


class OrderResponse(BaseModel):
    id: int
    total_amount: float
    payment_status: str
    items: list[OrderItemResponse]