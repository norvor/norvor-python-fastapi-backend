from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas
from ..db.session import get_db
from ..auth.security import get_current_user
from .. import models

router = APIRouter()

@router.post("/complete_onboarding", response_model=schemas.Organization)
def complete_organization_onboarding(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Mark the current user's organization's onboarding as complete.
    """
    if current_user.role != models.UserRole.EXECUTIVE:
        raise HTTPException(status_code=403, detail="Not authorized for this action")

    org = crud.complete_onboarding(db=db, org_id=current_user.organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org