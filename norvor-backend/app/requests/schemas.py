from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models import TicketStatus # Importing the Enum from models.py

# --- Ticket Schemas ---

class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    team_id: str

class TicketCreate(TicketBase):
    submitted_by: int

class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None

class Ticket(TicketBase):
    id: int
    submitted_by: int
    created_at: datetime
    status: TicketStatus

    class Config:
        from_attributes = True