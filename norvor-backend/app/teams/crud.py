from sqlalchemy.orm import Session
from uuid import UUID
from . import schemas
from .. import models

# Department CRUD
def create_department(db: Session, department: schemas.DepartmentCreate, org_id: int):
    """
    Creates a new Department and its associated DataBucket in a single transaction.
    """
    # Create the department instance
    db_department = models.Department(**department.dict(), organization_id=org_id)
    db.add(db_department)
    db.flush()  # Use flush to get the ID before the final commit

    # Create the associated data bucket
    db_bucket = models.DataBucket(department_id=db_department.id)
    db.add(db_bucket)
    
    db.commit()
    db.refresh(db_department)
    return db_department

def get_department(db: Session, department_id: UUID):
    return db.query(models.Department).filter(models.Department.id == department_id).first()

def get_departments_by_org(db: Session, org_id: int):
    return db.query(models.Department).filter(models.Department.organization_id == org_id).all()

# Team CRUD
def create_team(db: Session, team: schemas.TeamCreate):
    """
    Creates a new Team and its associated DataBowl.
    It finds the parent Department's DataBucket to link them correctly.
    """
    # Find the parent department's data bucket
    bucket = db.query(models.DataBucket).filter(models.DataBucket.department_id == team.department_id).first()
    if not bucket:
        # This would happen if a department was created without a bucket (the old bug)
        # You may need to reset your database one last time after this fix.
        raise Exception(f"DataBucket not found for department {team.department_id}")

    # Create the team instance
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.flush() # Use flush to get the team ID before committing

    # Create the associated data bowl
    db_bowl = models.DataBowl(
        team_id=db_team.id, 
        data_bucket_id=bucket.id,
        master_owner_team=db_team.id # A bowl is its own master by default
    )
    db.add(db_bowl)
    
    db.commit()
    db.refresh(db_team)
    return db_team

def get_team(db: Session, team_id: UUID):
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def get_teams_by_org(db: Session, org_id: int):
    return db.query(models.Team).join(models.Department).filter(models.Department.organization_id == org_id).all()

# TeamRole CRUD
def create_team_role(db: Session, team_role: schemas.TeamRoleCreate):
    """
    Creates a new TeamRole for a user and the associated DataCup.
    """
    # Find the data bowl for the team the user is being added to
    data_bowl = db.query(models.DataBowl).filter(models.DataBowl.team_id == team_role.team_id).first()
    if not data_bowl:
        raise Exception(f"DataBowl not found for team_id {team_role.team_id}")

    db_team_role = models.TeamRole(**team_role.dict())
    db.add(db_team_role)
    db.commit() # Commit the role first to get its ID
    db.refresh(db_team_role)
    
    # Create a datacup for the new team role
    create_data_cup(db, schemas.DataCupCreate(data_bowl_id=data_bowl.id, team_role_id=db_team_role.id))
    
    db.refresh(db_team_role) # Refresh again to load the relationship
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