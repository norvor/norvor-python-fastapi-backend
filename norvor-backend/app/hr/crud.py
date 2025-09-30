from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from . import schemas
from .. import models

# --- TimeOffRequest CRUD Functions ---

def create_time_off_request(db: Session, request: schemas.TimeOffRequestCreate):
    """
    Create a new time-off request in the database.
    """
    db_request = models.TimeOffRequest(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_time_off_request(db: Session, request_id: int):
    """
    Get a single time-off request by its ID.
    """
    return db.query(models.TimeOffRequest).filter(models.TimeOffRequest.id == request_id).first()

# --- MODIFY THIS FUNCTION ---
def get_time_off_requests_for_user(db: Session, user_id: UUID):
    """
    Get all time-off requests for a specific user.
    """
    return db.query(models.TimeOffRequest).filter(models.TimeOffRequest.user_id == user_id).all()
# --------------------------

# --- MODIFY THIS FUNCTION ---
# In get_all_time_off_requests function:
def get_all_time_off_requests(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.TimeOffRequest).join(models.User, models.TimeOffRequest.user_id == models.User.id).filter(models.User.organization_id == organization_id).offset(skip).limit(limit).all()

def update_time_off_request_status(db: Session, request_id: int, status: models.RequestStatus):
    """
    Update the status of a time-off request (e.g., approve, deny).
    """
    db_request = get_time_off_request(db, request_id)
    if db_request:
        db_request.status = status
        db.commit()
        db.refresh(db_request)
    return db_request