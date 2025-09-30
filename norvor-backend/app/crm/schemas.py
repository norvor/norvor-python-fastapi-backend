from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date
from uuid import UUID
from ..models import DealStage, ActivityType

# --- NEW COMPANY SCHEMAS ---
class CompanyBase(BaseModel):
    name: str
    domain: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    organization_id: int

    class Config:
        from_attributes = True
# -------------------------

# --- Contact Schemas (Updated) ---

class ContactBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class ContactCreate(ContactBase):
    owner_id: Optional[UUID] = None
    company_id: Optional[int] = None # Link to Company

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    owner_id: Optional[UUID] = None
    company_id: Optional[int] = None

class Contact(ContactBase):
    id: int
    owner_id: Optional[UUID] = None
    company_id: Optional[int] = None
    created_at: Optional[date] = None

    class Config:
        from_attributes = True

# --- Deal Schemas (Updated) ---

class DealBase(BaseModel):
    name: str
    value: float
    stage: DealStage
    close_date: date

class DealCreate(DealBase):
    owner_id: UUID
    contact_id: int
    company_id: int # Deals should also link to a company

class DealUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[float] = None
    stage: Optional[DealStage] = None
    close_date: Optional[date] = None
    owner_id: Optional[UUID] = None
    company_id: Optional[int] = None

class Deal(DealBase):
    id: int
    owner_id: UUID
    contact_id: int
    company_id: int

    class Config:
        from_attributes = True
        
# --- Activity Schemas (No Changes) ---

class ActivityBase(BaseModel):
    type: ActivityType
    notes: Optional[str] = None
    date: date
    contact_id: int
    user_id: UUID

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int

    class Config:
        from_attributes = True