from pydantic import BaseModel
from typing import Optional, Dict, Any
from ..models import OrganiserElementType

# --- OrganiserElement Schemas ---

class OrganiserElementBase(BaseModel):
    label: str
    type: OrganiserElementType
    properties: Dict[str, Any] = {}

class OrganiserElementCreate(OrganiserElementBase):
    parent_id: Optional[str] = None
    # --- ADD THIS LINE ---
    organization_id: int

class OrganiserElement(OrganiserElementBase):
    id: str
    parent_id: Optional[str] = None
    organization_id: int

    class Config:
        from_attributes = True