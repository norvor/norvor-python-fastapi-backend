from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from . import crud, schemas
from ..db.session import get_db
from ..auth.security import get_current_user
from .. import models

router = APIRouter()

# ===================================================================
# Department Endpoints
# ===================================================================
@router.post("/departments/", response_model=schemas.Department, status_code=status.HTTP_201_CREATED, summary="Create a new Department")
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_department(db=db, department=department, org_id=current_user.organization_id)

@router.get("/departments/", response_model=List[schemas.Department], summary="Get all Departments for the organization")
def read_departments(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_departments_by_org(db, org_id=current_user.organization_id)

@router.get("/departments/{department_id}", response_model=schemas.Department, summary="Get a single Department by ID")
def read_department(department_id: UUID, db: Session = Depends(get_db)):
    db_department = crud.get_department(db, department_id=department_id)
    if db_department is None: raise HTTPException(status_code=404, detail="Department not found")
    return db_department

@router.put("/departments/{department_id}", response_model=schemas.Department, summary="Update a Department's name")
def update_department(department_id: UUID, department: schemas.DepartmentUpdate, db: Session = Depends(get_db)):
    db_department = crud.update_department(db, department_id, department)
    if db_department is None: raise HTTPException(status_code=404, detail="Department not found")
    return db_department

@router.delete("/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a Department")
def delete_department(department_id: UUID, db: Session = Depends(get_db)):
    if not crud.delete_department(db, department_id):
        raise HTTPException(status_code=400, detail="Department not found or contains teams")

# ===================================================================
# Team Endpoints
# ===================================================================
@router.post("/teams/", response_model=schemas.Team, status_code=status.HTTP_201_CREATED, summary="Create a new Team")
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = crud.create_team(db=db, team=team)
    if not db_team: raise HTTPException(status_code=404, detail="Parent department not found")
    return db_team

@router.get("/teams/", response_model=List[schemas.Team], summary="Get all Teams in the organization")
def read_teams(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_teams_by_org(db, org_id=current_user.organization_id)

@router.get("/teams/{team_id}", response_model=schemas.Team, summary="Get a single Team by ID")
def read_team(team_id: UUID, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None: raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.put("/teams/{team_id}", response_model=schemas.Team, summary="Update a Team's properties")
def update_team(team_id: UUID, team: schemas.TeamUpdate, db: Session = Depends(get_db)):
    db_team = crud.update_team(db, team_id, team)
    if db_team is None: raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a Team")
def delete_team(team_id: UUID, db: Session = Depends(get_db)):
    if not crud.delete_team(db, team_id):
        raise HTTPException(status_code=404, detail="Team not found")

# ===================================================================
# TeamRole Endpoints
# ===================================================================
@router.post("/team_roles/", response_model=schemas.TeamRole, status_code=status.HTTP_201_CREATED, summary="Assign a User to a Team")
def create_team_role(team_role: schemas.TeamRoleCreate, db: Session = Depends(get_db)):
    db_role = crud.create_team_role(db=db, team_role=team_role)
    if not db_role: raise HTTPException(status_code=404, detail="Team not found for this role")
    return db_role

@router.put("/team_roles/{team_role_id}", response_model=schemas.TeamRole, summary="Update a User's role in a Team")
def update_team_role(team_role_id: UUID, team_role: schemas.TeamRoleUpdate, db: Session = Depends(get_db)):
    db_role = crud.update_team_role(db, team_role_id, team_role)
    if not db_role: raise HTTPException(status_code=404, detail="Team role not found")
    return db_role

@router.delete("/team_roles/{team_role_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove a User from a Team")
def delete_team_role(team_role_id: UUID, db: Session = Depends(get_db)):
    if not crud.delete_team_role(db, team_role_id):
        raise HTTPException(status_code=404, detail="Team role not found")

# ===================================================================
# Data Structure Read Endpoints (Buckets, Bowls, Cups)
# ===================================================================
@router.get("/data-buckets/{bucket_id}", response_model=schemas.DataBucket, summary="Get a Data Bucket by ID")
def read_data_bucket(bucket_id: UUID, db: Session = Depends(get_db)):
    db_bucket = crud.get_data_bucket(db, bucket_id)
    if not db_bucket: raise HTTPException(status_code=404, detail="Data Bucket not found")
    return db_bucket

@router.get("/data-bowls/{bowl_id}", response_model=schemas.DataBowl, summary="Get a Data Bowl by ID")
def read_data_bowl(bowl_id: UUID, db: Session = Depends(get_db)):
    db_bowl = crud.get_data_bowl(db, bowl_id)
    if not db_bowl: raise HTTPException(status_code=404, detail="Data Bowl not found")
    return db_bowl

@router.get("/data-cups/{cup_id}", response_model=schemas.DataCup, summary="Get a Data Cup by ID")
def read_data_cup(cup_id: UUID, db: Session = Depends(get_db)):
    db_cup = crud.get_data_cup(db, cup_id)
    if not db_cup: raise HTTPException(status_code=404, detail="Data Cup not found")
    return db_cup