from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class UserModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str = Field(..., min_length=1, max_length=100, example="John Doe")
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$', example="john@example.com")
    age: int = Field(..., ge=1, le=120, example=30)

    class Config:
        populate_by_name = True

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="John Doe")
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$', example="john@example.com")
    age: int = Field(..., ge=1, le=120, example=30)

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, example="Jane Doe")
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$', example="jane@example.com")
    age: Optional[int] = Field(None, ge=1, le=120, example=25)