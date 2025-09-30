from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from . import crud, schemas
from ..db.session import get_db
from ..users.crud import get_user 
from ..auth.security import get_current_user
from .. import models

router = APIRouter()

# --- NEW COMPANY ENDPOINTS ---
@router.post("/companies/", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_company(db=db, company=company, organization_id=current_user.organization_id)

@router.get("/companies/", response_model=List[schemas.Company])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    companies = crud.get_companies_by_organization(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return companies
# ---------------------------

# --- Contact Endpoints (No Changes) ---
@router.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)

# ... (rest of contact, deal, and activity endpoints remain the same)
@router.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Retrieve all contacts for the current user's organization.
    """
    contacts = crud.get_contacts(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
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

@router.post("/deals/", response_model=schemas.Deal)
def create_deal(deal: schemas.DealCreate, db: Session = Depends(get_db)):
    """
    Create a new deal.
    """
    owner = get_user(db, user_id=deal.owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail=f"User with id {deal.owner_id} not found")

    contact = crud.get_contact(db, contact_id=deal.contact_id) 
    if not contact:
        raise HTTPException(status_code=404, detail=f"Contact with id {deal.contact_id} not found")

    return crud.create_deal(db=db, deal=deal)

@router.get("/deals/", response_model=List[schemas.Deal])
def read_deals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Retrieve all deals for the current user's organization.
    """
    deals = crud.get_deals(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return deals

@router.put("/deals/{deal_id}", response_model=schemas.Deal)
def update_deal(deal_id: int, deal: schemas.DealUpdate, db: Session = Depends(get_db)):
    """
    Update an existing deal.
    """
    db_deal = crud.update_deal(db, deal_id=deal_id, deal_update=deal)
    if db_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return db_deal

@router.delete("/deals/{deal_id}", response_model=schemas.Deal)
def delete_deal(deal_id: int, db: Session = Depends(get_db)):
    """
    Delete a deal.
    """
    db_deal = crud.delete_deal(db, deal_id=deal_id)
    if db_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return db_deal


# --- Activity Endpoints ---
@router.post("/activities/", response_model=schemas.Activity)
def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    """
    Create a new activity.
    """
    return crud.create_activity(db=db, activity=activity)

@router.get("/activities/", response_model=List[schemas.Activity])
def read_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Retrieve all activities for the current user's organization.
    """
    activities = crud.get_activities(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return activities