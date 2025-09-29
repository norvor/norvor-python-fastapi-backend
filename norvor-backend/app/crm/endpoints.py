from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas
from ..db.session import get_db
from ..users.crud import get_user # We need this to validate the owner_id

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

# --- Deal Endpoints ---

@router.post("/deals/", response_model=schemas.Deal)
def create_deal(deal: schemas.DealCreate, db: Session = Depends(get_db)):
    """
    Create a new deal.
    """
    # Validate that the owner and contact exist before creating a deal
    owner = get_user(db, user_id=deal.owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail=f"User with id {deal.owner_id} not found")

    contact = crud.get_contacts(db, contact_id=deal.contact_id) # We'll add get_contact by id
    if not contact:
        raise HTTPException(status_code=404, detail=f"Contact with id {deal.contact_id} not found")

    return crud.create_deal(db=db, deal=deal)

@router.get("/deals/", response_model=List[schemas.Deal])
def read_deals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all deals.
    """
    deals = crud.get_deals(db, skip=skip, limit=limit)
    return deals