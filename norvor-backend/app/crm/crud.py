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

def get_deals(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of all deals.
    """
    return db.query(models.Deal).offset(skip).limit(limit).all()