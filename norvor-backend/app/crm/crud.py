# norvor-backend/app/crm/crud.py
from sqlalchemy.orm import Session
from . import schemas
from .. import models
import datetime

# --- Contact CRUD Functions ---

def create_contact(db: Session, contact: schemas.ContactCreate):
    """
    Create a new contact in the database.
    """
    db_contact = models.Contact(
        **contact.dict(),
        created_at=datetime.date.today()
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of all contacts.
    """
    return db.query(models.Contact).offset(skip).limit(limit).all()


# --- Deal CRUD Functions ---

def create_deal(db: Session, deal: schemas.DealCreate):
    """
    Create a new deal in the database.
    """
    db_deal = models.Deal(**deal.dict())
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal

def get_contact(db: Session, contact_id: int):
    """
    Get a single contact by their ID.
    """
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def update_contact(db: Session, contact_id: int, contact_update: schemas.ContactCreate):
    """
    Update an existing contact's details.
    """
    db_contact = get_contact(db, contact_id=contact_id)
    if db_contact:
        update_data = contact_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    """
    Delete a contact from the database.
    """
    db_contact = get_contact(db, contact_id=contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact    

def get_deals(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of all deals.
    """
    return db.query(models.Deal).offset(skip).limit(limit).all()


# --- Activity CRUD Functions (MUST BE PRESENT) ---
def create_activity(db: Session, activity: schemas.ActivityCreate):
    """
    Create a new activity in the database.
    """
    db_activity = models.Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_activities(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of all activities.
    """
    return db.query(models.Activity).offset(skip).limit(limit).all()