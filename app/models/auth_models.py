from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    email: str = Field(..., example="john@example.com")
    password: str = Field(..., min_length=6, example="password123")
    
class UserRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="John Doe")
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$', example="john@example.com")
    age: int = Field(..., ge=1, le=120, example=30)
    password: str = Field(..., min_length=6, example="password123")

class ResponseToken(BaseModel):
    access_token: str
    token_type: str = "bearer"