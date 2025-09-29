import sys
from pathlib import Path

# Step 1: Add the project root to Python's path.
# This ensures that Python can find the 'app' module.
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

print(f"Project root added to path: {project_root}")

# Step 2: Now we can safely import from our app.
from app.db.session import engine
from app.db.base_class import Base


# Step 3: We MUST explicitly import every model class here.
# This is the most important step. It tells SQLAlchemy's Base object
# about every table we want to create.
print("Importing all models...")
from app.models import (
    User,
    Organization,
    Contact,
    Deal,
    Project,
    Task,
    TimeOffRequest,
    OrganiserElement,
    Doc,
    Ticket
)
print("Models imported successfully.")


def init_db():
    print("Connecting to the database and creating all tables...")
    try:
        # This command now knows about all your tables and will create them.
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully! Your database is ready.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    init_db()