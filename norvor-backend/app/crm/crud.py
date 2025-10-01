from sqlalchemy.orm import Session
from . import schemas
from .. import models
import datetime
from uuid import UUID


# --- Company CRUD Functions ---
def create_company(db: Session, company: schemas.CompanyCreate, organization_id: int):
    db_company = models.Company(**company.dict(), organization_id=organization_id)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

def get_companies_by_organization(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Company).filter(models.Company.organization_id == organization_id).offset(skip).limit(limit).all()

# --- Contact CRUD Functions ---
def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(
        **contact.dict(),
        created_at=datetime.date.today()
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def get_contacts(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).join(models.User, models.Contact.owner_id == models.User.id).filter(models.User.organization_id == organization_id).offset(skip).limit(limit).all()

def update_contact(db: Session, contact_id: int, contact_update: schemas.ContactUpdate):
    db_contact = get_contact(db, contact_id=contact_id)
    if db_contact:
        update_data = contact_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id=contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact    

# --- Deal CRUD Functions ---
def create_deal(db: Session, deal: schemas.DealCreate):
    db_deal = models.Deal(**deal.dict())
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal

def get_deal(db: Session, deal_id: int):
    return db.query(models.Deal).filter(models.Deal.id == deal_id).first()

def get_deals(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Deal).join(models.User, models.Deal.owner_id == models.User.id).filter(models.User.organization_id == organization_id).offset(skip).limit(limit).all()

def update_deal(db: Session, deal_id: int, deal_update: schemas.DealUpdate):
    db_deal = get_deal(db, deal_id=deal_id)
    if db_deal:
        update_data = deal_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_deal, key, value)
        db.commit()
        db.refresh(db_deal)
    return db_deal

def delete_deal(db: Session, deal_id: int):
    db_deal = get_deal(db, deal_id=deal_id)
    if db_deal:
        db.delete(db_deal)
        db.commit()
    return db_deal

# --- Activity CRUD Functions ---
def create_activity(db: Session, activity: schemas.ActivityCreate):
    db_activity = models.Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_activities(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Activity).join(models.User, models.Activity.user_id == models.User.id).filter(models.User.organization_id == organization_id).offset(skip).limit(limit).all()

# --- NEW OPTIMIZED FUNCTION ---
def get_deals_for_user(db: Session, user_id: UUID):
    """
    Get all deals for a user in a single, optimized query using JOINs.
    """
    return db.query(models.Deal).join(models.DataCup).join(models.TeamRole).filter(models.TeamRole.user_id == user_id).all()

def get_contacts_for_user(db: Session, user_id: UUID):
    """
    Get all contacts for a user in a single, optimized query using JOINs.
    """
    return db.query(models.Contact).join(models.DataCup).join(models.TeamRole).filter(models.TeamRole.user_id == user_id).all()

# --- CRM TASK CRUD FUNCTIONS ---
def create_crm_task(db: Session, task: schemas.CrmTaskCreate):
    db_task = models.CrmTask(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_crm_tasks(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.CrmTask).join(models.User, models.CrmTask.owner_id == models.User.id).filter(models.User.organization_id == organization_id).offset(skip).limit(limit).all()