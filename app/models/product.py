from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class ProductModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str = Field(..., min_length=1, max_length=200, example="iPhone 15")
    description: str = Field(..., min_length=1, max_length=1000, example="Latest iPhone model")
    price: float = Field(..., gt=0, example=999.99)
    category: str = Field(..., min_length=1, max_length=100, example="Electronics")
    stock: int = Field(..., ge=0, example=50)
    user_id: str = Field(..., example="user123")

    class Config:
        populate_by_name = True

class ProductResponse(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: str
    price: float
    category: str
    stock: int
    user_id: str

    class Config:
        populate_by_name = True

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, example="iPhone 15")
    description: str = Field(..., min_length=1, max_length=1000, example="Latest iPhone model")
    price: float = Field(..., gt=0, example=999.99)
    category: str = Field(..., min_length=1, max_length=100, example="Electronics")
    stock: int = Field(..., ge=0, example=50)

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200, example="iPhone 15 Pro")
    description: Optional[str] = Field(None, min_length=1, max_length=1000, example="Updated description")
    price: Optional[float] = Field(None, gt=0, example=1099.99)
    category: Optional[str] = Field(None, min_length=1, max_length=100, example="Electronics")
    stock: Optional[int] = Field(None, ge=0, example=30)