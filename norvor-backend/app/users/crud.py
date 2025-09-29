from sqlalchemy.orm import Session
from . import schemas
from .. import models
from ..auth.security import get_password_hash

def get_user(db: Session, user_id: int):
    """
    Get a single user by their ID.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    Get a single user by their email address.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of users, with pagination (skip and limit).
    """
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new organization and a new user as its first member (public signup).
    """
    # 1. Create the Organization
    db_org = models.Organization(name=user.organization_name)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)

    # 2. Hash the user's password
    hashed_password = get_password_hash(user.password)
    
    # 3. Create the User, linking them to the new organization
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        organization_id=db_org.id, # Link to the organization
        role=models.UserRole.EXECUTIVE, 
        department=user.department,
        title=user.title
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# --- ADD THIS NEW FUNCTION ---
def create_user_by_admin(db: Session, user: schemas.UserCreateByAdmin, organization_id: int):
    """
    Create a new user as an admin, automatically linking them to the admin's organization.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        organization_id=organization_id, # Use the admin's org ID
        role=user.role,
        department=user.department,
        title=user.title
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
# ------------------------------

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
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