from sqlalchemy.orm import Session
from typing import List

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

def get_time_off_requests_for_user(db: Session, user_id: int):
    """
    Get all time-off requests for a specific user.
    """
    return db.query(models.TimeOffRequest).filter(models.TimeOffRequest.user_id == user_id).all()

def get_all_time_off_requests(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of all time-off requests (for admin/HR Manager views).
    """
    return db.query(models.TimeOffRequest).offset(skip).limit(limit).all()

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