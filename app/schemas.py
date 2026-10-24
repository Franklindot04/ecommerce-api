from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

from app.models import OrderStatus, PaymentStatus


# -------------------------
# PRODUCT
# -------------------------


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total: int = Field(ge=0)
    total_pages: int = Field(ge=0)


# -------------------------
# CART
# -------------------------


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    id: int
    quantity: int
    product: ProductResponse
    model_config = ConfigDict(from_attributes=True)


# -------------------------
# ORDERS
# -------------------------


class OrderItemResponse(BaseModel):
    id: int
    quantity: int
    price_at_purchase: float
    product: ProductResponse
    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemResponse]
    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


# -------------------------
# PAYMENTS
# -------------------------


class PaymentCreate(BaseModel):
    order_id: int


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    status: PaymentStatus
    provider: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PaymentWebhookPayload(BaseModel):
    payment_id: int
    status: PaymentStatus


# -------------------------
# AUTH
# -------------------------


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
