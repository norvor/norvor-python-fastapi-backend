import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parent))

from app.database import Base, engine

# --- CRUCIAL FIX ---
# We must explicitly import all the models here so that
# SQLAlchemy's 'Base' object knows about them.
from app.models import User, Organization, Contact, Deal, Project, Task, TimeOffRequest, OrganiserElement, Doc, Ticket
# -------------------

def init_db():
    print("Creating all database tables...")
    # This command connects to the DB and creates all tables
    # that inherit from 'Base' in your models.py file.
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init_db()