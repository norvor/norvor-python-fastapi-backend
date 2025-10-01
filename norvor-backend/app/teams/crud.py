from sqlalchemy.orm import Session
from uuid import UUID
from . import schemas
from .. import models

# Department CRUD
def create_department(db: Session, department: schemas.DepartmentCreate, org_id: int):
    db_department = models.Department(**department.dict(), organization_id=org_id)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def get_department(db: Session, department_id: UUID):
    return db.query(models.Department).filter(models.Department.id == department_id).first()

def get_departments_by_org(db: Session, org_id: int):
    return db.query(models.Department).filter(models.Department.organization_id == org_id).all()

# Team CRUD
def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_team(db: Session, team_id: UUID):
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def get_teams_by_org(db: Session, org_id: int):
    return db.query(models.Team).join(models.Department).filter(models.Department.organization_id == org_id).all()

# TeamRole CRUD
def create_team_role(db: Session, team_role: schemas.TeamRoleCreate):
    db_team_role = models.TeamRole(**team_role.dict())
    db.add(db_team_role)
    db.commit()
    db.refresh(db_team_role)
    # Create a datacup for the new team role
    create_data_cup(db, schemas.DataCupCreate(team_id=db_team_role.team_id, team_role_id=db_team_role.id))
    return db_team_role

def get_team_role(db: Session, team_role_id: UUID):
    return db.query(models.TeamRole).filter(models.TeamRole.id == team_role_id).first()

def delete_team_role(db: Session, team_role_id: UUID):
    db_team_role = get_team_role(db, team_role_id)
    if db_team_role:
        # Unassign datacup
        data_cup = db.query(models.DataCup).filter(models.DataCup.team_role_id == team_role_id).first()
        if data_cup:
            data_cup.team_role_id = None
            db.commit()
        db.delete(db_team_role)
        db.commit()
    return db_team_role


# DataCup CRUD
def create_data_cup(db: Session, data_cup: schemas.DataCupCreate):
    db_data_cup = models.DataCup(**data_cup.dict())
    db.add(db_data_cup)
    db.commit()
    db.refresh(db_data_cup)
    return db_data_cup

def get_data_cup(db: Session, data_cup_id: UUID):
    return db.query(models.DataCup).filter(models.DataCup.id == data_cup_id).first()

def assign_data_cup(db: Session, data_cup_id: UUID, team_role_id: UUID):
    db_data_cup = get_data_cup(db, data_cup_id)
    if db_data_cup:
        db_data_cup.team_role_id = team_role_id
        db.commit()
        db.refresh(db_data_cup)
    return db_data_cup