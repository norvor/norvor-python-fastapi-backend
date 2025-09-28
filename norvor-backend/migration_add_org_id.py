import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parent))

from app.database import SessionLocal
from app import models

def run_migration():
    db = SessionLocal()
    try:
        print("Starting migration to add organization ID to users...")

        # 1. Find or create the default organization
        default_org_name = "Norvorx Default"
        default_org = db.query(models.Organization).filter(models.Organization.name == default_org_name).first()

        if not default_org:
            print(f"Creating default organization: {default_org_name}")
            default_org = models.Organization(name=default_org_name)
            db.add(default_org)
            db.commit()
            db.refresh(default_org)

        print(f"Using Organization ID: {default_org.id}")

        # 2. Find all users without an organization ID
        users_to_update = db.query(models.User).filter(models.User.organization_id == None).all()

        if not users_to_update:
            print("No users to update. All users already have an organization ID.")
            return

        print(f"Found {len(users_to_update)} users to update.")

        # 3. Update each user
        for user in users_to_update:
            user.organization_id = default_org.id

        db.commit()
        print("Successfully assigned organization ID to all users.")

    finally:
        db.close()

if __name__ == "__main__":
    run_migration()