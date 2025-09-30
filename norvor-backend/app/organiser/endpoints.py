from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas
from ..db.session import get_db
from ..auth.security import get_current_user
from .. import models


router = APIRouter()

# --- MODIFIED THIS ENDPOINT ---
@router.post("/elements/", response_model=schemas.OrganiserElement)
def create_organiser_element(
    element_in: schemas.OrganiserElementCreateIn, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new element in the company structure for the current user's organization.
    """
    # Create the full data object, including the organization_id from the current user
    element_create = schemas.OrganiserElementCreate(
        **element_in.dict(),
        organization_id=current_user.organization_id
    )
    return crud.create_organiser_element(db=db, element=element_create)
# ---------------------------


@router.get("/elements/", response_model=List[schemas.OrganiserElement])
def read_organiser_elements(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve all elements in the company structure for the current user's organization.
    """
    elements = crud.get_organiser_elements(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return elements


@router.put("/elements/{element_id}", response_model=schemas.OrganiserElement)
def update_organiser_element(
    element_id: str, 
    element_in: schemas.OrganiserElementCreateIn, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Update an element's properties, label, or parent.
    """
    element_update = schemas.OrganiserElementCreate(
        **element_in.dict(),
        organization_id=current_user.organization_id
    )
    db_element = crud.update_organiser_element(db, element_id=element_id, element_update=element_update)
    if db_element is None:
        raise HTTPException(status_code=404, detail="Element not found")
    return db_element


@router.delete("/elements/{element_id}", response_model=schemas.OrganiserElement)
def delete_organiser_element(element_id: str, db: Session = Depends(get_db)):
    """
    Delete an element from the company structure.
    """
    db_element = crud.delete_organiser_element(db, element_id=element_id)
    if db_element is None:
        raise HTTPException(status_code=404, detail="Element not found")
    return db_element