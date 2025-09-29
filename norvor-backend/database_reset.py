import sys
from pathlib import Path

# Add the project root to Python's path to allow for imports
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

print("--- Database Reset Script ---")

from app.db.session import engine
from app.db.base import Base # This now imports all your models

print("Dropping all existing tables...")
# This command will connect to your database and issue DROP TABLE commands
Base.metadata.drop_all(bind=engine)
print("Tables dropped successfully.")

print("Creating new tables based on current models...")
# This command will create all tables according to your latest models.py
Base.metadata.create_all(bind=engine)
print("✅ All tables created successfully. Your database schema is now up to date.")