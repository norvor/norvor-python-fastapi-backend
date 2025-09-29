from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas
from ..db.session import get_db
from ..auth.security import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    print("=" * 50)
    print("SIGNUP DEBUG START")
    print(f"Name: {user.name}")
    print(f"Email: {user.email}")
    print(f"Password: {user.password}")
    print(f"Password length: {len(user.password)}")
    print(f"Department: {user.department}")
    print(f"Role: {user.role}")
    
    # Check if email already exists
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            print(f"❌ Email already registered: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        print("✅ Email is available")
        
        # Try to create the user
        print("🔨 Attempting to create user...")
        created_user = crud.create_user(db=db, user=user)
        print(f"✅ User created successfully with ID: {created_user.id}")
        
        return created_user
        
    except HTTPException as he:
        print(f"💥 HTTP Exception: {he.detail}")
        raise he
    except Exception as e:
        print(f"💥 Unexpected error during signup: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        print("SIGNUP DEBUG END")
        print("=" * 50)


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all users.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    """
    Fetch the currently logged-in user.
    """
    return current_user

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single user by ID.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user_details(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Update an existing user's details (Used for role and permission management).
    """
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

