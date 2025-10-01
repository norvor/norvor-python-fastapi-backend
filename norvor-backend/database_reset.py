import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the project root to Python's path to allow for imports
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

print("--- Database Reset Script with CASCADE ---")

from app.db.session import engine
from app.db.base import Base # This now imports all your models

def reset_database_with_cascade():
    """
    Drops all tables with CASCADE and then recreates them.
    This is a destructive operation.
    """
    # Get a list of all table names from the metadata
    table_names = Base.metadata.tables.keys()

    with engine.connect() as connection:
        # The connection is transactional by default
        with connection.begin() as transaction:
            try:
                print("Dropping all existing tables with CASCADE...")
                for table_name in table_names:
                    # Use "IF EXISTS" to prevent errors if a table is already gone
                    # Use double quotes to handle case-sensitive table names
                    drop_query = text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')
                    print(f"Executing: {drop_query}")
                    connection.execute(drop_query)
                
                transaction.commit()
                print("Tables dropped successfully.")

            except Exception as e:
                print(f"An error occurred during table dropping: {e}")
                transaction.rollback()
                return # Exit if dropping failed

    print("\nCreating new tables based on current models...")
    try:
        # This command will create all tables according to your latest models
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully. Your database schema is now up to date.")
    except Exception as e:
        print(f"An error occurred during table creation: {e}")

if __name__ == "__main__":
    # Optional: Add a confirmation step to prevent accidental data loss
    confirm = input("Are you sure you want to completely wipe and reset the database? (y/n): ")
    if confirm.lower() == 'y':
        reset_database_with_cascade()
    else:
        print("Database reset cancelled.")