from pydantic import BaseModel
from typing import Optional
from uuid import UUID

# --- Document Schemas ---

class DocBase(BaseModel):
    title: str
    icon: Optional[str] = "📄"
    content: Optional[str] = ""

class DocCreate(DocBase):
    parent_id: Optional[str] = None
    organization_id: int
    data_cup_id: UUID # <-- ADD THIS

class DocUpdate(DocBase):
    parent_id: Optional[str] = None

class Doc(DocBase):
    id: str
    parent_id: Optional[str] = None
    organization_id: int
    data_cup_id: UUID # <-- ADD THIS
    
    class Config:
        from_attributes = True