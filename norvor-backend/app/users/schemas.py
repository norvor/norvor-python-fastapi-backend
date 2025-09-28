from pydantic import BaseModel, EmailStr
from typing import Optional
from ..models import UserRole

# --- Properties to receive via API on creation ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str  # ADD THIS LINE
    role: UserRole = UserRole.TEAM # Default new users to 'Team' role
    department: str
    avatar: Optional[str] = None
    title: Optional[str] = None

# --- Properties to return via API ---
# IMPORTANT: Notice this schema does NOT include the password.
# We never want to send the password hash back to the client.
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