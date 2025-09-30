from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from ..models import OrganiserElementType

class OrganiserElementBase(BaseModel):
    label: str
    type: OrganiserElementType
    properties: Dict[str, Any] = {}

# --- NEW SCHEMA FOR INCOMING DATA ---
class OrganiserElementCreateIn(OrganiserElementBase):
    parent_id: Optional[str] = None
# ------------------------------------

# This schema is now used internally by our logic
class OrganiserElementCreate(OrganiserElementBase):
    parent_id: Optional[str] = None
    organization_id: int

class OrganiserElement(OrganiserElementBase):
    id: str
    parent_id: Optional[str] = None
    organization_id: int

    class Config:
        from_attributes = True