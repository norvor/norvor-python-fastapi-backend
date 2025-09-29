from pydantic import BaseModel
from typing import Optional
from datetime import date
from uuid import UUID # --- ADD THIS IMPORT ---
from ..models import DealStage, ActivityType
from .. import models

# --- Contact Schemas ---

class ContactBase(BaseModel):
    name: str
    company: str
    email: str
    phone: str

class ContactCreate(ContactBase):
    # --- MODIFY THIS LINE ---
    owner_id: Optional[UUID] = None
    # ----------------------

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    # --- MODIFY THIS LINE ---
    owner_id: Optional[UUID] = None
    # ----------------------

class Contact(ContactBase):
    id: int
    # --- MODIFY THIS LINE ---
    owner_id: Optional[UUID] = None
    # ----------------------
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
    # --- MODIFY THIS LINE ---
    owner_id: UUID
    # ----------------------
    contact_id: int

class DealUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[float] = None
    stage: Optional[DealStage] = None
    close_date: Optional[date] = None
    # --- MODIFY THIS LINE ---
    owner_id: Optional[UUID] = None
    # ----------------------

class Deal(DealBase):
    id: int
    # --- MODIFY THIS LINE ---
    owner_id: UUID
    # ----------------------
    contact_id: int

    class Config:
        from_attributes = True
        
# --- Activity Schemas ---

class ActivityBase(BaseModel):
    type: models.ActivityType
    notes: Optional[str] = None
    date: date
    contact_id: int
    # --- MODIFY THIS LINE ---
    user_id: UUID
    # ----------------------

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int

    class Config:
        from_attributes = True