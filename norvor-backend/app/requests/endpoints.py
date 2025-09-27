from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas
from .. import models
from ..database import get_db
from ..users.crud import get_user # To validate the submitter exists

router = APIRouter()

@router.post("/tickets/", response_model=schemas.Ticket)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    """
    Create a new ticket.
    """
    # Validate that the user submitting the ticket exists
    db_user = get_user(db, user_id=ticket.submitted_by)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with id {ticket.submitted_by} not found")

    return crud.create_ticket(db=db, ticket=ticket)


@router.get("/tickets/team/{team_id}", response_model=List[schemas.Ticket])
def read_tickets_for_team(team_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all tickets for a specific team.
    """
    tickets = crud.get_tickets_by_team(db, team_id=team_id, skip=skip, limit=limit)
    return tickets


@router.patch("/tickets/{ticket_id}/status", response_model=schemas.Ticket)
def update_ticket_status(ticket_id: int, status_update: schemas.TicketUpdate, db: Session = Depends(get_db)):
    """
    Update the status of a ticket (e.g., to 'In Progress' or 'Closed').
    """
    if status_update.status is None:
        raise HTTPException(status_code=400, detail="No status provided for update")
        
    db_ticket = crud.update_ticket_status(db, ticket_id=ticket_id, status=status_update.status)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket