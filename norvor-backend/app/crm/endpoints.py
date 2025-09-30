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

# --- Company Endpoints ---
@router.post("/companies/", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_company(db=db, company=company, organization_id=current_user.organization_id)

@router.get("/companies/", response_model=List[schemas.Company])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    companies = crud.get_companies_by_organization(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return companies

# --- Contact Endpoints ---
@router.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)

@router.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    contacts = crud.get_contacts(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return contacts

# ... (other contact endpoints)

# --- Deal Endpoints ---
@router.post("/deals/", response_model=schemas.Deal)
def create_deal(deal: schemas.DealCreate, db: Session = Depends(get_db)):
    return crud.create_deal(db=db, deal=deal)

@router.get("/deals/", response_model=List[schemas.Deal])
def read_deals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    deals = crud.get_deals(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return deals

# ... (other deal endpoints)

# --- Activity Endpoints ---
@router.post("/activities/", response_model=schemas.Activity)
def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    return crud.create_activity(db=db, activity=activity)

@router.get("/activities/", response_model=List[schemas.Activity])
def read_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    activities = crud.get_activities(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return activities

# --- CRM TASK ENDPOINTS ---
@router.post("/tasks/", response_model=schemas.CrmTask)
def create_crm_task(task: schemas.CrmTaskCreate, db: Session = Depends(get_db)):
    return crud.create_crm_task(db=db, task=task)

@router.get("/tasks/", response_model=List[schemas.CrmTask])
def read_crm_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    tasks = crud.get_crm_tasks(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return tasks