import sys
from pathlib import Path
import uuid # --- ADD THIS IMPORT ---

# Add the project's root directory to the Python path.
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app import models
from app.auth.security import get_password_hash
from datetime import datetime, date

# --- GENERATE STATIC UUIDs FOR USERS ---
user_ids = {
    "anya": uuid.uuid4(),
    "ben": uuid.uuid4(),
    "chloe": uuid.uuid4(),
    "david": uuid.uuid4(),
    "eva": uuid.uuid4()
}
# ------------------------------------

ORGANIZATION_DATA = { "id": 1, "name": "QuantumLeap Dynamics" }

# --- UPDATE ALL FOREIGN KEYS TO USE THE STATIC UUIDs ---
ACTIVITIES_DATA = [
    {"id": 1001, "type": "Call", "notes": "Initial discovery call with Fintech Innovators.", "date": date(2025, 9, 20), "contact_id": 101, "user_id": user_ids["chloe"]},
    {"id": 1002, "type": "Email", "notes": "Sent Project Phoenix proposal to Fintech.", "date": date(2025, 9, 25), "contact_id": 101, "user_id": user_ids["chloe"]},
    {"id": 1003, "type": "Meeting", "notes": "Met with HealthBridge team to discuss integration.", "date": date(2025, 9, 28), "contact_id": 102, "user_id": user_ids["chloe"]},
]

USERS_DATA = [
    {"id": user_ids["anya"], "name": "Anya Sharma", "email": "anya.sharma@quantumleap.dev", "role": "Executive", "title": "Chief Executive Officer", "department": "Executive", "avatar": "https://i.pravatar.cc/150?u=anya.sharma", "organization_id": 1},
    {"id": user_ids["ben"], "name": "Ben Carter", "email": "ben.carter@quantumleap.dev", "role": "Management", "title": "VP of Sales", "department": "Sales", "avatar": "https://i.pravatar.cc/150?u=ben.carter", "organization_id": 1},
    {"id": user_ids["chloe"], "name": "Chloe Davis", "email": "chloe.davis@quantumleap.dev", "role": "Team", "title": "Account Executive", "department": "Sales", "manager_id": user_ids["ben"], "avatar": "https://i.pravatar.cc/150?u=chloe.davis", "organization_id": 1},
    {"id": user_ids["david"], "name": "David Rodriguez", "email": "david.r@quantumleap.dev", "role": "Management", "title": "Engineering Lead", "department": "Engineering", "avatar": "https://i.pravatar.cc/150?u=david.r", "organization_id": 1},
    {"id": user_ids["eva"], "name": "Eva Martinez", "email": "eva.martinez@quantumleap.dev", "role": "Team", "title": "Senior Frontend Developer", "department": "Engineering", "manager_id": user_ids["david"], "avatar": "https://i.pravatar.cc/150?u=eva.martinez", "organization_id": 1},
]
CONTACTS_DATA = [
    {"id": 101, "name": "Fintech Innovators Inc.", "company": "Fintech Innovators", "email": "contact@fintechinnovate.com", "phone": "+91 22 4567 8901", "owner_id": user_ids["chloe"], "created_at": date(2025, 8, 15)},
    {"id": 102, "name": "HealthBridge Solutions", "company": "HealthBridge", "email": "support@healthbridge.io", "phone": "+91 80 1234 5678", "owner_id": user_ids["chloe"], "created_at": date(2025, 9, 1)},
]
DEALS_DATA = [
    {"id": 201, "name": "Project Phoenix - Platform Overhaul", "value": 250000.00, "stage": "Negotiation", "contact_id": 101, "owner_id": user_ids["chloe"], "close_date": date(2025, 10, 30)},
    {"id": 202, "name": "Patient Data API Integration", "value": 120000.00, "stage": "Proposal Sent", "contact_id": 102, "owner_id": user_ids["chloe"], "close_date": date(2025, 11, 20)},
]
PROJECTS_DATA = [
    {"id": 301, "name": "Q4 Product Launch: 'Odyssey'", "manager_id": user_ids["david"], "status": "On Track", "progress": 65, "start_date": date(2025, 9, 1), "end_date": date(2025, 12, 15), "member_ids": [str(user_ids["eva"])]},
]
TASKS_DATA = [
    {"id": 401, "name": "Finalize UI/UX Mockups", "description": "Complete all Figma mockups for the Odyssey dashboard.", "status": "In Progress", "assignee_id": user_ids["eva"], "project_id": 301, "due_date": date(2025, 10, 10)},
    {"id": 402, "name": "Setup Staging Environment", "description": "Deploy the latest build to the staging server for QA.", "status": "To Do", "assignee_id": user_ids["eva"], "project_id": 301, "due_date": date(2025, 10, 15)},
]
TIMEOFF_DATA = [
    {"id": 501, "user_id": user_ids["eva"], "type": "Vacation", "start_date": date(2025, 10, 20), "end_date": date(2025, 10, 24), "status": "Approved", "reason": "Diwali family trip."},
]
ORGANISER_DATA = [
    {"id": "org_root", "parent_id": None, "type": "Department", "label": "QuantumLeap Dynamics", "properties": {"CEO": "Anya Sharma"}},
    {"id": "dept_sales", "parent_id": "org_root", "type": "Department", "label": "Sales", "properties": {"Head": "Ben Carter"}},
    {"id": "team_sales_west", "parent_id": "dept_sales", "type": "Team", "label": "West Coast Sales", "properties": {}},
]
DOCS_DATA = [
    {"id": "doc_onboarding", "parent_id": None, "title": "🚀 Welcome to QuantumLeap!", "icon": "🚀", "content": "<h1>Your journey starts here.</h1><p>This is the central knowledge base.</p>"},
]
TICKETS_DATA = [
    {"id": 601, "title": "Access to Figma designs for 'Odyssey'", "description": "Hey team, I can't seem to access the latest mockups for the Q4 launch.", "status": "Open", "submitted_by": user_ids["eva"], "team_id": "alpha_squad", "created_at": datetime(2025, 9, 28, 10, 0, 0)},
]

# -------------------------------------------------------------------

def seed_database(db: Session):
    print("Clearing old data (in correct dependency order)...")
    db.query(models.Activity).delete()
    db.query(models.Ticket).delete()
    db.query(models.Doc).delete()
    db.query(models.OrganiserElement).delete()
    db.query(models.TimeOffRequest).delete()
    db.query(models.Task).delete()
    db.query(models.Project).delete()
    db.query(models.Deal).delete()
    db.query(models.Contact).delete()
    db.query(models.User).delete()
    db.query(models.Organization).delete()
    db.commit()

    print("Seeding new data...")
    db_org = models.Organization(**ORGANIZATION_DATA)
    db.add(db_org)
    db.commit()

    for user_data in USERS_DATA:
        db_user = models.User(
            **user_data,
            hashed_password="password123"
        )
        db.add(db_user)
    db.commit()

    for contact_data in CONTACTS_DATA:
        db.add(models.Contact(**contact_data))
    db.commit()

    for deal_data in DEALS_DATA:
        db.add(models.Deal(**deal_data))
    db.commit()
    
    for project_data in PROJECTS_DATA:
        db.add(models.Project(**project_data))
    db.commit()

    for task_data in TASKS_DATA:
        db.add(models.Task(**task_data))
    db.commit()

    for request_data in TIMEOFF_DATA:
        db.add(models.TimeOffRequest(**request_data))
    db.commit()
    
    for element_data in ORGANISER_DATA:
        db.add(models.OrganiserElement(**element_data))
    db.commit()
    
    for doc_data in DOCS_DATA:
        db.add(models.Doc(**doc_data))
    db.commit()
    
    for ticket_data in TICKETS_DATA:
        db.add(models.Ticket(**ticket_data))
    db.commit()

    for activity_data in ACTIVITIES_DATA:
        db.add(models.Activity(**activity_data))
    db.commit()

    print("\n✅ Database seeding complete!")
    print("You can log in with any user's email (e.g., 'anya.sharma@quantumleap.dev').")
    print("The password for all users is: password123")


if __name__ == "__main__":
    print("--- Starting Database Seeding ---")
    db_session = SessionLocal()
    try:
        seed_database(db_session)
    except Exception as e:
        print(f"\nAn error occurred during seeding: {e}")
        import traceback
        traceback.print_exc()
        db_session.rollback()
    finally:
        db_session.close()
        print("--- Seeding process finished. ---")