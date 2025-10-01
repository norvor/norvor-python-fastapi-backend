# app/db/base.py
from .base_class import Base

# Import all the models, so they are registered with the Base.
from ..models import (
    User, 
    Organization, 
    Contact, 
    Deal, 
    Project, 
    Task, 
    TimeOffRequest, 
    Doc, 
    Ticket,
    Department,
    Team,
    TeamRole,
    DataCup,
    DataBowl
)