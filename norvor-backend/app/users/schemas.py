from pydantic import BaseModel, EmailStr
from typing import Optional
from ..models import UserRole # Assuming UserRole is in the global models.py

# --- Properties to receive via API on creation ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    department: str
    avatar: Optional[str] = None
    title: Optional[str] = None

# --- Properties to return via API ---
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    department: str
    avatar: Optional[str] = None
    title: Optional[str] = None

    class Config:
        from_attributes = True