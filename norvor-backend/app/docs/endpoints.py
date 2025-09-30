from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas
from ..db.session import get_db
from ..auth.security import get_current_user # --- ADD THIS IMPORT ---
from .. import models # --- ADD THIS IMPORT ---

router = APIRouter()

# --- MODIFY THIS ENDPOINT ---
@router.post("/", response_model=schemas.Doc)
def create_doc(doc: schemas.DocCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Create a new document for the current user's organization.
    """
    doc.organization_id = current_user.organization_id
    return crud.create_doc(db=db, doc=doc)
# ---------------------------


# --- MODIFY THIS ENDPOINT ---
@router.get("/", response_model=List[schemas.Doc])
def read_all_docs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Retrieve all documents for the current user's organization.
    """
    docs = crud.get_all_docs(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return docs


@router.get("/{doc_id}", response_model=schemas.Doc)
def read_doc(doc_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single document by its ID.
    """
    db_doc = crud.get_doc(db, doc_id=doc_id)
    if db_doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_doc


@router.put("/{doc_id}", response_model=schemas.Doc)
def update_doc(doc_id: str, doc: schemas.DocUpdate, db: Session = Depends(get_db)):
    """
    Update a document's title, content, icon, or parent.
    """
    db_doc = crud.update_doc(db, doc_id=doc_id, doc_update=doc)
    if db_doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_doc


@router.delete("/{doc_id}", response_model=schemas.Doc)
def delete_doc(doc_id: str, db: Session = Depends(get_db)):
    """
    Delete a document.
    """
    db_doc = crud.delete_doc(db, doc_id=doc_id)
    if db_doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_doc