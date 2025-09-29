from pydantic import BaseModel
from typing import Optional

class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    has_completed_onboarding: bool

    class Config:
        from_attributes = True