from pydantic import BaseModel
from typing import Optional
from datetime import date
from ..models import DealStage # Importing the Enum from our central models file

# --- Contact Schemas ---

class ContactBase(BaseModel):
    name: str
    company: str
    email: str
    phone: str

class ContactCreate(ContactBase):
    owner_id: Optional[int] = None

class Contact(ContactBase):
    id: int
    owner_id: Optional[int] = None
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
    owner_id: int
    contact_id: int

class Deal(DealBase):
    id: int
    owner_id: int
    contact_id: int

    class Config:
        from_attributes = True