from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=8, max_length=100, description="Senha do usuário")
    full_name: str = Field(..., min_length=3, max_length=255, description="Nome completo")
    is_admin: bool = Field(False, description="Se o usuário é administrador")
    
    @validator('password')
    def validate_password(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('A senha deve conter pelo menos um número')
        if not any(char.isupper() for char in v):
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula')
        if not any(char.islower() for char in v):
            raise ValueError('A senha deve conter pelo menos uma letra minúscula')
        return v

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., description="Senha do usuário")

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    is_admin: bool
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
