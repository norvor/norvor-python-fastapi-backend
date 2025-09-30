from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from . import crud, schemas
from .. import models
from ..db.session import get_db
from ..users.crud import get_user
from ..auth.security import get_current_user # --- ADD THIS IMPORT ---

router = APIRouter()

@router.post("/requests/", response_model=schemas.TimeOffRequest)
def create_time_off_request(request: schemas.TimeOffRequestCreate, db: Session = Depends(get_db)):
    """
    Create a new time-off request for a user.
    """
    db_user = get_user(db, user_id=request.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with id {request.user_id} not found")

    return crud.create_time_off_request(db=db, request=request)


# --- MODIFY THIS ENDPOINT ---
@router.get("/requests/", response_model=List[schemas.TimeOffRequest])
def read_all_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    requests = crud.get_all_time_off_requests(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return requests
# ---------------------------


@router.get("/requests/user/{user_id}", response_model=List[schemas.TimeOffRequest])
def read_requests_for_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve all time-off requests for a specific user.
    """
    requests = crud.get_time_off_requests_for_user(db, user_id=user_id)
    return requests


@router.patch("/requests/{request_id}/status", response_model=schemas.TimeOffRequest)
def update_request_status(request_id: int, status: models.RequestStatus, db: Session = Depends(get_db)):
    """
    Update the status of a time-off request (e.g., to 'Approved' or 'Denied').
    """
    db_request = crud.update_time_off_request_status(db, request_id=request_id, status=status)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Time-off request not found")
    return db_request