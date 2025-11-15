from sqlalchemy.orm import Session
from .. import models
from . import schemas

def get_organization(db: Session, org_id: int):
    """
    Get a single organization by its ID.
    """
    return db.query(models.Organization).filter(models.Organization.id == org_id).first()

def complete_onboarding(db: Session, org_id: int):
    """
    Mark an organization's onboarding as complete.
    """
    db_org = get_organization(db, org_id=org_id)
    if db_org:
        db_org.has_completed_onboarding = True
        db.commit()
        db.refresh(db_org)
    return db_org

