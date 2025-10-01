from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from . import crud, schemas
from ..db.session import get_db
from ..auth.security import get_current_user
from .. import models

router = APIRouter()

# Departments
@router.post("/departments/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_department(db=db, department=department, org_id=current_user.organization_id)

@router.get("/departments/", response_model=List[schemas.Department])
def read_departments(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_departments_by_org(db, org_id=current_user.organization_id)

# Teams
@router.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    return crud.create_team(db=db, team=team)

@router.get("/teams/{team_id}", response_model=schemas.Team)
def read_team(team_id: UUID, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

# TeamRoles
@router.post("/team_roles/", response_model=schemas.TeamRole)
def create_team_role(team_role: schemas.TeamRoleCreate, db: Session = Depends(get_db)):
    return crud.create_team_role(db=db, team_role=team_role)

@router.delete("/team_roles/{team_role_id}", response_model=schemas.TeamRole)
def delete_team_role(team_role_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_system_administrator and current_user.role != models.UserRole.EXECUTIVE:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.delete_team_role(db, team_role_id)

# DataCups
@router.put("/datacups/{data_cup_id}/assign/{team_role_id}", response_model=schemas.DataCup)
def assign_data_cup(data_cup_id: UUID, team_role_id: UUID, db: Session = Depends(get_db)):
    return crud.assign_data_cup(db, data_cup_id=data_cup_id, team_role_id=team_role_id)