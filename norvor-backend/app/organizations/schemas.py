from pydantic import BaseModel
from typing import Optional

class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    pass

# --- ADD THIS NEW SCHEMA ---
class OrganizationInUser(OrganizationBase):
    id: int
    has_completed_onboarding: bool

    class Config:
        from_attributes = True
# ---------------------------

class Organization(OrganizationBase):
    id: int
    has_completed_onboarding: bool

    class Config:
        from_attributes = True