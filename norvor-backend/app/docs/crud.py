from sqlalchemy.orm import Session
from typing import List
import uuid

from . import schemas
from .. import models
from uuid import UUID


def create_doc(db: Session, doc: schemas.DocCreate):
    """
    Create a new document.
    """
    generated_id = f"doc_{uuid.uuid4().hex}"
    
    db_doc = models.Doc(
        **doc.dict(),
        id=generated_id
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def get_doc(db: Session, doc_id: str):
    """
    Get a single document by its ID.
    """
    return db.query(models.Doc).filter(models.Doc.id == doc_id).first()

# --- MODIFY THIS FUNCTION ---
def get_all_docs(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    """
    Get a list of all documents for a specific organization.
    """
    return db.query(models.Doc).filter(models.Doc.organization_id == organization_id).offset(skip).limit(limit).all()
# ---------------------------

def update_doc(db: Session, doc_id: str, doc_update: schemas.DocUpdate):
    """
    Update a document's title, content, icon, or parent.
    """
    db_doc = get_doc(db, doc_id=doc_id)
    if db_doc:
        update_data = doc_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_doc, key, value)
        db.commit()
        db.refresh(db_doc)
    return db_doc

def get_docs_for_user(db: Session, user_id: UUID):
    """
    Get all documents for a user in a single, optimized query using JOINs.
    """
    return db.query(models.Doc).join(models.DataCup).join(models.TeamRole).filter(models.TeamRole.user_id == user_id).all()



def delete_doc(db: Session, doc_id: str):
    """
    Delete a document.
    """
    db_doc = get_doc(db, doc_id=doc_id)
    if db_doc:
        db.delete(db_doc)
        db.commit()
    return db_doc