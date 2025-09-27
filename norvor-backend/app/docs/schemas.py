from pydantic import BaseModel
from typing import Optional

# --- Document Schemas ---

class DocBase(BaseModel):
    title: str
    icon: Optional[str] = "📄" # Default icon
    content: Optional[str] = ""

class DocCreate(DocBase):
    parent_id: Optional[str] = None

class DocUpdate(DocBase):
    parent_id: Optional[str] = None

class Doc(DocBase):
    id: str
    parent_id: Optional[str] = None

    class Config:
        from_attributes = True