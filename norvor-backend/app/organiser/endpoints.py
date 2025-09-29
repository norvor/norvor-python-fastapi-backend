from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas
from ..db.session import get_db

router = APIRouter()

@router.post("/elements/", response_model=schemas.OrganiserElement)
def create_organiser_element(element: schemas.OrganiserElementCreate, db: Session = Depends(get_db)):
    """
    Create a new element in the company structure.
    """
    return crud.create_organiser_element(db=db, element=element)


@router.get("/elements/", response_model=List[schemas.OrganiserElement])
def read_organiser_elements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all elements in the company structure.
    """
    elements = crud.get_organiser_elements(db, skip=skip, limit=limit)
    return elements


@router.put("/elements/{element_id}", response_model=schemas.OrganiserElement)
def update_organiser_element(element_id: str, element: schemas.OrganiserElementCreate, db: Session = Depends(get_db)):
    """
    Update an element's properties, label, or parent.
    """
    db_element = crud.update_organiser_element(db, element_id=element_id, element_update=element)
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