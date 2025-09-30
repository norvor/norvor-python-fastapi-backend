from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID
from ..models import DealStage, ActivityType, CrmTaskStatus # Import CrmTaskStatus

# --- Company Schemas ---
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

# --- Contact Schemas ---
class ContactBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class ContactCreate(ContactBase):
    owner_id: Optional[UUID] = None
    company_id: Optional[int] = None

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

# --- Deal Schemas ---
class DealBase(BaseModel):
    name: str
    value: float
    stage: DealStage
    close_date: date

class DealCreate(DealBase):
    owner_id: UUID
    contact_id: int
    company_id: int

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
        
# --- Activity Schemas ---
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

# --- NEW CRM TASK SCHEMAS ---
class CrmTaskBase(BaseModel):
    title: str
    due_date: datetime
    status: CrmTaskStatus = CrmTaskStatus.NOT_STARTED

class CrmTaskCreate(CrmTaskBase):
    owner_id: UUID
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None

class CrmTaskUpdate(BaseModel):
    title: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[CrmTaskStatus] = None
    owner_id: Optional[UUID] = None

class CrmTask(CrmTaskBase):
    id: int
    owner_id: UUID
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None

    class Config:
        from_attributes = True