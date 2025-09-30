from pydantic import BaseModel
from typing import Optional, List

class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    pass

# --- ADD THE SCHEMAS BELOW ---

class SidebarModule(BaseModel):
    id: str
    name: str

class SidebarItem(BaseModel):
    id: str
    name: str
    modules: List[SidebarModule]

class SidebarGroup(BaseModel):
    title: str
    items: List[SidebarItem]

class SidebarConfig(BaseModel):
    groups: List[SidebarGroup]

# --------------------------

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