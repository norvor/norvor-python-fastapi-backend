from sqlalchemy.orm import Session
from typing import List
import uuid

from . import schemas
from .. import models

def create_doc(db: Session, doc: schemas.DocCreate):
    """
    Create a new document.
    """
    # Generate a unique string ID for the new document
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

def get_all_docs(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of all documents.
    """
    return db.query(models.Doc).offset(skip).limit(limit).all()

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

def delete_doc(db: Session, doc_id: str):
    """
    Delete a document.
    """
    db_doc = get_doc(db, doc_id=doc_id)
    if db_doc:
        # In a real app, you might want to handle child documents here
        # (e.g., delete them or make them root documents).
        db.delete(db_doc)
        db.commit()
    return db_doc