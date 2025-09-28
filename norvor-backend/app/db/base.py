# app/db/base.py
from sqlalchemy.orm import declarative_base

# 1. This is the DeclarativeMeta instance that all models will inherit from.
from .base_class import Base

# 2. Import all the models, so they are registered with the Base.
# This is the single most important part of the fix.
from ..models import User, Organization, Contact, Deal, Project, Task, TimeOffRequest, OrganiserElement, Doc, Ticket