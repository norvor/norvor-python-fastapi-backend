from pydantic import BaseModel
from typing import Optional, Dict, Any
from ..models import OrganiserElementType # Importing the Enum from models.py

# --- OrganiserElement Schemas ---

class OrganiserElementBase(BaseModel):
    label: str
    type: OrganiserElementType
    properties: Dict[str, Any] = {}

class OrganiserElementCreate(OrganiserElementBase):
    parent_id: Optional[str] = None

class OrganiserElement(OrganiserElementBase):
    id: str
    parent_id: Optional[str] = None

    class Config:
        from_attributes = True