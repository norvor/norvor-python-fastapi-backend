from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date
from .models import UserRole, DealStage


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    department: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class ContactBase(BaseModel):
    name: str
    company: str
    email: EmailStr
    phone: str


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    id: int
    owner_id: Optional[int] = None

    class Config:
        orm_mode = True


class DealBase(BaseModel):
    name: str
    value: float
    stage: DealStage
    close_date: date


class DealCreate(DealBase):
    pass


class Deal(DealBase):
    id: int
    contact_id: int
    owner_id: int

    class Config:
        orm_mode = True