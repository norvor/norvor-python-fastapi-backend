from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID # --- ADD THIS IMPORT ---

from . import crud, schemas
from ..db.session import get_db
from ..users.crud import get_user 

router = APIRouter()

# --- Contact Endpoints ---

@router.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    """
    Create a new contact.
    """
    return crud.create_contact(db=db, contact=contact)

@router.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all contacts.
    """
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts

@router.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single contact by its ID.
    """
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    """
    Update an existing contact.
    """
    db_contact = crud.update_contact(db, contact_id=contact_id, contact_update=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/contacts/{contact_id}", response_model=schemas.Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Delete a contact.
    """
    db_contact = crud.delete_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

# --- Deal Endpoints ---

# --- MODIFY THIS ENDPOINT ---
@router.post("/deals/", response_model=schemas.Deal)
def create_deal(deal: schemas.DealCreate, db: Session = Depends(get_db)):
    """
    Create a new deal.
    """
    # Now correctly fetches a user by UUID
    owner = get_user(db, user_id=deal.owner_id)