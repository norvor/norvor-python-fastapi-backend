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
    Create a new user in the database.
    """
    # Hash the plain text password from the frontend
    hashed_password = get_password_hash(user.password)
    
    # Create the user model instance with the hashed password
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        role=user.role,
        department=user.department,
        avatar=user.avatar,
        title=user.title
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user