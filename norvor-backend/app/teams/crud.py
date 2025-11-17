from sqlalchemy.orm import Session, joinedload
from uuid import UUID
from . import schemas
from .. import models

# ===================================================================
# Department CRUD
# ===================================================================
def get_department(db: Session, department_id: UUID):
    return db.query(models.Department).options(joinedload(models.Department.teams), joinedload(models.Department.data_bucket)).filter(models.Department.id == department_id).first()

def get_departments_by_org(db: Session, org_id: int):
    return db.query(models.Department).filter(models.Department.organization_id == org_id).options(joinedload(models.Department.teams), joinedload(models.Department.data_bucket)).all()

def create_department(db: Session, department: schemas.DepartmentCreate, org_id: int):
    db_department = models.Department(**department.dict(), organization_id=org_id)
    db.add(db_department)
    db.flush()
    db_bucket = models.DataBucket(department_id=db_department.id)
    db.add(db_bucket)
    db.commit()
    db.refresh(db_department)
    return db_department

def update_department(db: Session, department_id: UUID, department_update: schemas.DepartmentUpdate):
    db_department = get_department(db, department_id)
    if db_department:
        if department_update.name is not None:
            db_department.name = department_update.name
        db.commit()
        db.refresh(db_department)
    return db_department

def delete_department(db: Session, department_id: UUID):
    db_department = get_department(db, department_id)
    if db_department and not db_department.teams and not db_department.immutable:
        db.delete(db_department)
        db.commit()
        return db_department
    return None

# ===================================================================
# Team CRUD
# ===================================================================
def get_team(db: Session, team_id: UUID):
    return db.query(models.Team).options(joinedload(models.Team.team_roles).joinedload(models.TeamRole.user), joinedload(models.Team.data_bowl)).filter(models.Team.id == team_id).first()

def get_teams_by_org(db: Session, org_id: int):
    return db.query(models.Team).join(models.Department).filter(models.Department.organization_id == org_id).all()

def create_team(db: Session, team: schemas.TeamCreate):
    bucket = db.query(models.DataBucket).filter(models.DataBucket.department_id == team.department_id).first()
    if not bucket: return None
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.flush()
    db_bowl = models.DataBowl(team_id=db_team.id, data_bucket_id=bucket.id, master_owner_team=db_team.id)
    db.add(db_bowl)
    db.commit()
    db.refresh(db_team)
    return db_team

def update_team(db: Session, team_id: UUID, team_update: schemas.TeamUpdate):
    db_team = get_team(db, team_id=team_id)
    if db_team:
        update_data = team_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_team, key, value)
        db.commit()
        db.refresh(db_team)
    return db_team

def delete_team(db: Session, team_id: UUID):
    db_team = get_team(db, team_id)
    if db_team and not db_team.immutable:
        db.delete(db_team)
        db.commit()
        return db_team
    return None

# ===================================================================
# TeamRole CRUD
# ===================================================================
def get_team_role(db: Session, team_role_id: UUID):
    return db.query(models.TeamRole).filter(models.TeamRole.id == team_role_id).first()
    
def create_team_role(db: Session, team_role: schemas.TeamRoleCreate):
    data_bowl = db.query(models.DataBowl).filter(models.DataBowl.team_id == team_role.team_id).first()
    if not data_bowl: return None
    db_team_role = models.TeamRole(**team_role.dict())
    db.add(db_team_role)
    db.commit()
    db.refresh(db_team_role)
    create_data_cup(db, schemas.DataCupCreate(data_bowl_id=data_bowl.id, team_role_id=db_team_role.id))
    db.refresh(db_team_role)
    return db_team_role

def update_team_role(db: Session, team_role_id: UUID, team_role_update: schemas.TeamRoleUpdate):
    db_team_role = get_team_role(db, team_role_id)
    if db_team_role:
        if team_role_update.role is not None:
            db_team_role.role = team_role_update.role
        db.commit()
        db.refresh(db_team_role)
    return db_team_role

def delete_team_role(db: Session, team_role_id: UUID):
    db_team_role = get_team_role(db, team_role_id)
    if db_team_role:
        data_cup = db.query(models.DataCup).filter(models.DataCup.team_role_id == team_role_id).first()
        if data_cup: db.delete(data_cup)
        db.delete(db_team_role)
        db.commit()
    return db_team_role

# ===================================================================
# DataBucket, DataBowl, DataCup Read Operations
# ===================================================================
def get_data_bucket(db: Session, data_bucket_id: UUID):
    return db.query(models.DataBucket).options(joinedload(models.DataBucket.data_bowls)).filter(models.DataBucket.id == data_bucket_id).first()

def get_data_bowl(db: Session, data_bowl_id: UUID):
    return db.query(models.DataBowl).options(joinedload(models.DataBowl.data_cups)).filter(models.DataBowl.id == data_bowl_id).first()

def get_data_cup(db: Session, data_cup_id: UUID):
    return db.query(models.DataCup).filter(models.DataCup.id == data_cup_id).first()

def create_data_cup(db: Session, data_cup: schemas.DataCupCreate):
    db_data_cup = models.DataCup(**data_cup.dict())
    db.add(db_data_cup)
    db.commit()
    db.refresh(db_data_cup)
    return db_data_cup