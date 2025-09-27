from pydantic import BaseModel
from typing import Optional
from datetime import date
from ..models import LeaveType, RequestStatus # Importing Enums from models.py

# --- TimeOffRequest Schemas ---

class TimeOffRequestBase(BaseModel):
    start_date: date
    end_date: date
    reason: Optional[str] = None
    type: LeaveType

class TimeOffRequestCreate(TimeOffRequestBase):
    user_id: int
    status: RequestStatus = RequestStatus.PENDING # Default status on creation

class TimeOffRequest(TimeOffRequestBase):
    id: int
    user_id: int
    status: RequestStatus

    class Config:
        from_attributes = True