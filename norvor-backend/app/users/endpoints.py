from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from . import crud, schemas
from ..db.session import get_db
from ..auth.security import get_current_user
from .. import models

router = APIRouter()

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    """
    Fetch the currently logged-in user.
    """
    return current_user

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user and organization.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.post("/create_by_admin", response_model=schemas.User)
def create_user_by_admin(
    user: schemas.UserCreateByAdmin, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new user within the current admin's organization.
    """
    if current_user.role != models.UserRole.EXECUTIVE:
        raise HTTPException(status_code=403, detail="Not authorized to create users")
        
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    return crud.create_user_by_admin(db=db, user=user, organization_id=current_user.organization_id)

# --- MODIFY THIS ENDPOINT ---
@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve all users for the current user's organization.
    """
    users = crud.get_users(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return users
# ---------------------------

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a single user by ID.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user_details(user_id: UUID, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Update an existing user's details.
    """
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user