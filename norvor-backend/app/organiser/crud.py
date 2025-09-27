from sqlalchemy.orm import Session
from typing import List
import uuid

from . import schemas
from .. import models

def create_organiser_element(db: Session, element: schemas.OrganiserElementCreate):
    """
    Create a new organiser element.
    """
    # Generate a unique ID for the new element
    generated_id = f"el_{uuid.uuid4().hex}"
    
    db_element = models.OrganiserElement(
        **element.dict(),
        id=generated_id
    )
    db.add(db_element)
    db.commit()
    db.refresh(db_element)
    return db_element

def get_organiser_elements(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of all organiser elements.
    """
    return db.query(models.OrganiserElement).offset(skip).limit(limit).all()

def update_organiser_element(db: Session, element_id: str, element_update: schemas.OrganiserElementCreate):
    """
    Update an organiser element's properties or parent.
    """
    db_element = db.query(models.OrganiserElement).filter(models.OrganiserElement.id == element_id).first()
    if db_element:
        update_data = element_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_element, key, value)
        db.commit()
        db.refresh(db_element)
    return db_element

def delete_organiser_element(db: Session, element_id: str):
    """
    Delete an organiser element.
    """
    db_element = db.query(models.OrganiserElement).filter(models.OrganiserElement.id == element_id).first()
    if db_element:
        db.delete(db_element)
        db.commit()
    return db_element