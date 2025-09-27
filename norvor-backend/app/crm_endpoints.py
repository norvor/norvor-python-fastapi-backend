# --- ADD THESE ---
@router.post("/deals/", response_model=schemas.Deal)
def create_deal(deal: schemas.DealCreate, owner_id: int, contact_id: int, db: Session = Depends(get_db)):
    # Optional: Check if owner and contact exist before creating a deal
    db_owner = crud.get_user(db, user_id=owner_id)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")

    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return crud.create_deal(db=db, deal=deal, owner_id=owner_id, contact_id=contact_id)


@router.get("/deals/", response_model=List[schemas.Deal])
def read_deals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    deals = crud.get_deals(db, skip=skip, limit=limit)
    return deals