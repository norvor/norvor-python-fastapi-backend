from pydantic import BaseModel
from typing import Optional
from datetime import date
from uuid import UUID # --- ADD THIS IMPORT ---
from ..models import LeaveType, RequestStatus

# --- TimeOffRequest Schemas ---

class TimeOffRequestBase(BaseModel):
    start_date: date
    end_date: date
    reason: Optional[str] = None
    type: LeaveType

class TimeOffRequestCreate(TimeOffRequestBase):
    # --- MODIFY THIS LINE ---
    user_id: UUID
    # ----------------------
    status: RequestStatus = RequestStatus.PENDING

class TimeOffRequest(TimeOffRequestBase):
    id: int
    # --- MODIFY THIS LINE ---
    user_id: UUID
    # ----------------------
    status: RequestStatus

    class Config:
        from_attributes = True