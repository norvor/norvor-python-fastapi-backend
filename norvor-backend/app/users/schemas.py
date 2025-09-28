from pydantic import BaseModel, EmailStr
from typing import Optional
from ..models import UserRole

# --- Properties to receive via API on creation ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    organization_name: str # ADD THIS LINE
    role: UserRole = UserRole.TEAM
    department: str = "General" # Default new users to 'General' department
    title: Optional[str] = "Team Member" # Default title

# --- Properties to return via API ---
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    organization_id: int # ADD THIS LINE
    department: str
    avatar: Optional[str] = None
    title: Optional[str] = None

    class Config:
        from_attributes = True