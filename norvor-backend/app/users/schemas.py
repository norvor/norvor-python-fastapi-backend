from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID # --- ADD THIS IMPORT ---
from ..models import UserRole

# --- Properties to receive via API on public creation ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    organization_name: str 
    role: UserRole = UserRole.TEAM
    department: str = "General" 
    title: Optional[str] = "Team Member" 

# Properties for an Admin creating a user within their own org
class UserCreateByAdmin(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole
    department: str
    title: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    department: Optional[str] = None
    title: Optional[str] = None
    organization_id: Optional[int] = None


# --- Properties to return via API ---
class User(BaseModel):
    # --- MODIFY THIS LINE ---
    id: UUID
    # ----------------------
    name: str
    email: EmailStr
    role: UserRole
    organization_id: int
    department: str
    avatar: Optional[str] = None
    title: Optional[str] = None

    class Config:
        from_attributes = True