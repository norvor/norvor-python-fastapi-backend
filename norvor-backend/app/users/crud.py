from sqlalchemy.orm import Session
from uuid import UUID
from . import schemas
from .. import models
from ..auth.security import get_password_hash
from ..teams.crud import create_department, create_team, create_team_role

def get_user(db: Session, user_id: UUID):
    """
    Get a single user by their ID.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    Get a single user by their email address.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    """
    Get a list of users for a specific organization, with pagination.
    """
    return db.query(models.User).filter(models.User.organization_id == organization_id).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new organization and a new user as its first member (public signup).
    """
    db_org = models.Organization(name=user.organization_name)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)

    hashed_password = get_password_hash(user.password)
    # Create invisible user
    invisible_user = models.User(
        name=f"{db_org.name}-admin",
        email=f"admin@{db_org.name.lower().replace(' ', '')}.norvor.com",
        hashed_password=hashed_password,
        organization_id=db_org.id,
        role=models.UserRole.EXECUTIVE,
    )
    db.add(invisible_user)
    db.commit()
    db.refresh(invisible_user)

    # Create default department and teams
    store_dept = create_department(db, department=schemas.DepartmentCreate(name="Store"), org_id=db_org.id)
    warm_team = create_team(db, team=schemas.TeamCreate(name="Warm", department_id=store_dept.id, immutable=True))
    cold_team = create_team(db, team=schemas.TeamCreate(name="Cold", department_id=store_dept.id, immutable=True))
    
    # Add invisible user to teams
    create_team_role(db, team_role=schemas.TeamRoleCreate(user_id=invisible_user.id, team_id=warm_team.id))
    create_team_role(db, team_role=schemas.TeamRoleCreate(user_id=invisible_user.id, team_id=cold_team.id))


    hashed_password = user.password
    
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        organization_id=db_org.id,
        role=models.UserRole.EXECUTIVE, 
        department=user.department,
        title=user.title
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def create_user_by_admin(db: Session, user: schemas.UserCreateByAdmin, organization_id: int):
    """
    Create a new user as an admin, automatically linking them to the admin's organization.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        organization_id=organization_id,
        role=user.role,
        department=user.department,
        title=user.title
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_datacups(db: Session, user_id: UUID):
    """
    Get all DataCup IDs associated with a user through their team roles.
    """
    team_roles = db.query(models.TeamRole).filter(models.TeamRole.user_id == user_id).all()
    datacup_ids = []
    for role in team_roles:
        if role.data_cup:
            datacup_ids.append(role.data_cup.id)
    return datacup_ids

def update_user(db: Session, user_id: UUID, user_update: schemas.UserUpdate):
    """
    Update an existing user's details (e.g., role, name).
    """
    db_user = get_user(db, user_id=user_id)
    if db_user:
        update_data = user_update.dict(exclude_unset=True, exclude_none=True)
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
            
        db.commit()
        db.refresh(db_user)
    return db_user