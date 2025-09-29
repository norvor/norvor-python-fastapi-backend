from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID # --- ADD THIS IMPORT ---
from ..models import TicketStatus

# --- Ticket Schemas ---

class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    team_id: str

class TicketCreate(TicketBase):
    # --- MODIFY THIS LINE ---
    submitted_by: UUID
    # ----------------------

class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None

class Ticket(TicketBase):
    id: int
    # --- MODIFY THIS LINE ---
    submitted_by: UUID
    # ----------------------
    created_at: datetime
    status: TicketStatus

    class Config:
        from_attributes = True