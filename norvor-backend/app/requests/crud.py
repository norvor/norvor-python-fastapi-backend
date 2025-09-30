from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from . import schemas
from .. import models

def create_ticket(db: Session, ticket: schemas.TicketCreate):
    """
    Create a new ticket in the database.
    """
    db_ticket = models.Ticket(
        **ticket.dict(),
        created_at=datetime.utcnow(),
        status=models.TicketStatus.OPEN
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket(db: Session, ticket_id: int):
    """
    Get a single ticket by its ID.
    """
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

def get_tickets_by_team(db: Session, team_id: str, skip: int = 0, limit: int = 100):
    """
    Get all tickets for a specific team.
    """
    return db.query(models.Ticket).filter(models.Ticket.team_id == team_id).offset(skip).limit(limit).all()

def update_ticket_status(db: Session, ticket_id: int, status: models.TicketStatus):
    """
    Update the status of a ticket.
    """
    db_ticket = get_ticket(db, ticket_id=ticket_id)
    if db_ticket:
        db_ticket.status = status
        db.commit()
        db.refresh(db_ticket)
    return db_ticket

# --- MODIFY THIS FUNCTION ---
def get_all_tickets(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    """
    Get a list of all tickets for a specific organization.
    """
    return db.query(models.Ticket).join(models.User, models.Ticket.submitted_by == models.User.id).filter(models.User.organization_id == organization_id).offset(skip).limit(limit).all()
# --------------------------