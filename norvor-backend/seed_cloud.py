import sys
from pathlib import Path
import uuid

# Add the project's root directory to the Python path.
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app import models
from app.auth.security import get_password_hash
from datetime import datetime, date, timedelta

# --- STATIC UUIDs FOR CONSISTENT RELATIONSHIPS ---
user_ids = {
    "anya": uuid.uuid4(),      # Executive
    "ben": uuid.uuid4(),        # Sales Manager
    "david": uuid.uuid4(),      # Eng Lead
    "chloe": uuid.uuid4(),      # Sales Rep 1
    "liam": uuid.uuid4(),       # Sales Rep 2
    "eva": uuid.uuid4(),        # Eng Developer 1
    "mason": uuid.uuid4(),      # Eng Developer 2
}

# --- DATA DICTIONARIES ---

ORGANIZATION_DATA = { "name": "QuantumLeap Dynamics" }

USERS_DATA = [
    # Executive
    {"id": user_ids["anya"], "name": "Anya Sharma", "email": "anya.sharma@quantumleap.dev", "role": models.UserRole.EXECUTIVE, "title": "Chief Executive Officer", "department": "Executive", "avatar": "https://i.pravatar.cc/150?u=anya.sharma"},
    
    # Management
    {"id": user_ids["ben"], "name": "Ben Carter", "email": "ben.carter@quantumleap.dev", "role": models.UserRole.MANAGEMENT, "title": "VP of Sales", "department": "Sales", "manager_id": user_ids["anya"], "avatar": "https://i.pravatar.cc/150?u=ben.carter"},
    {"id": user_ids["david"], "name": "David Rodriguez", "email": "david.r@quantumleap.dev", "role": models.UserRole.MANAGEMENT, "title": "Engineering Lead", "department": "Engineering", "manager_id": user_ids["anya"], "avatar": "https://i.pravatar.cc/150?u=david.r"},

    # Team Members
    {"id": user_ids["chloe"], "name": "Chloe Davis", "email": "chloe.davis@quantumleap.dev", "role": models.UserRole.TEAM, "title": "Senior Account Executive", "department": "Sales", "manager_id": user_ids["ben"], "avatar": "https://i.pravatar.cc/150?u=chloe.davis"},
    {"id": user_ids["liam"], "name": "Liam Goldberg", "email": "liam.goldberg@quantumleap.dev", "role": models.UserRole.TEAM, "title": "Account Executive", "department": "Sales", "manager_id": user_ids["ben"], "avatar": "https://i.pravatar.cc/150?u=liam.goldberg"},
    {"id": user_ids["eva"], "name": "Eva Martinez", "email": "eva.martinez@quantumleap.dev", "role": models.UserRole.TEAM, "title": "Senior Frontend Developer", "department": "Engineering", "manager_id": user_ids["david"], "avatar": "https://i.pravatar.cc/150?u=eva.martinez"},
    {"id": user_ids["mason"], "name": "Mason Lee", "email": "mason.lee@quantumleap.dev", "role": models.UserRole.TEAM, "title": "Backend Developer", "department": "Engineering", "manager_id": user_ids["david"], "avatar": "https://i.pravatar.cc/150?u=mason.lee"},
]

COMPANIES_DATA = [
    {"id": 1, "name": "Fintech Innovators Inc.", "domain": "fintechinnovate.com"},
    {"id": 2, "name": "HealthBridge Solutions", "domain": "healthbridge.io"},
    {"id": 3, "name": "NextGen Logistics", "domain": "nextgenlogistics.com"},
    {"id": 4, "name": "Terra Solar", "domain": "terrasolar.com"},
]

CONTACTS_DATA = [
    {"id": 101, "name": "Priya Singh", "email": "priya.singh@fintechinnovate.com", "phone": "+91 22 4567 8901", "owner_id": user_ids["chloe"], "company_id": 1, "created_at": date.today() - timedelta(days=45)},
    {"id": 102, "name": "Rohan Mehta", "email": "rohan.mehta@healthbridge.io", "phone": "+91 80 1234 5678", "owner_id": user_ids["chloe"], "company_id": 2, "created_at": date.today() - timedelta(days=30)},
    {"id": 103, "name": "Anjali Rao", "email": "anjali.rao@nextgenlogistics.com", "phone": "+91 44 9876 5432", "owner_id": user_ids["liam"], "company_id": 3, "created_at": date.today() - timedelta(days=20)},
    {"id": 104, "name": "Vikram Desai", "email": "vikram.desai@terrasolar.com", "phone": "+91 11 2345 6789", "owner_id": user_ids["liam"], "company_id": 4, "created_at": date.today() - timedelta(days=10)},
    {"id": 105, "name": "Suresh Gupta", "email": "suresh.gupta@fintechinnovate.com", "phone": "+91 22 4567 8902", "owner_id": user_ids["chloe"], "company_id": 1, "created_at": date.today() - timedelta(days=5)},
]

DEALS_DATA = [
    {"id": 201, "name": "Project Phoenix - Platform Overhaul", "value": 250000.00, "stage": models.DealStage.NEGOTIATION, "company_id": 1, "contact_id": 101, "owner_id": user_ids["chloe"], "close_date": date.today() + timedelta(days=30)},
    {"id": 202, "name": "Patient Data API Integration", "value": 120000.00, "stage": models.DealStage.PROPOSAL_SENT, "company_id": 2, "contact_id": 102, "owner_id": user_ids["chloe"], "close_date": date.today() + timedelta(days=45)},
    {"id": 203, "name": "Supply Chain Automation Suite", "value": 180000.00, "stage": models.DealStage.NEW_LEAD, "company_id": 3, "contact_id": 103, "owner_id": user_ids["liam"], "close_date": date.today() + timedelta(days=60)},
    {"id": 204, "name": "Solar Panel Fleet Management Software", "value": 95000.00, "stage": models.DealStage.WON, "company_id": 4, "contact_id": 104, "owner_id": user_ids["liam"], "close_date": date.today() - timedelta(days=15)},
    {"id": 205, "name": "Fintech Security Audit", "value": 45000.00, "stage": models.DealStage.LOST, "company_id": 1, "contact_id": 105, "owner_id": user_ids["chloe"], "close_date": date.today() - timedelta(days=5)},
]

CRM_TASKS_DATA = [
    {"title": "Follow up on Project Phoenix proposal", "due_date": datetime.now() + timedelta(days=2), "status": models.CrmTaskStatus.NOT_STARTED, "owner_id": user_ids["chloe"], "deal_id": 201},
    {"title": "Schedule demo for HealthBridge API", "due_date": datetime.now() + timedelta(days=5), "status": models.CrmTaskStatus.NOT_STARTED, "owner_id": user_ids["chloe"], "deal_id": 202},
    {"title": "Send initial outreach email to Anjali Rao", "due_date": datetime.now() - timedelta(days=1), "status": models.CrmTaskStatus.COMPLETED, "owner_id": user_ids["liam"], "contact_id": 103},
]

ACTIVITIES_DATA = [
    {"type": models.ActivityType.CALL, "notes": "Initial discovery call with Priya. Discussed key pain points around their legacy system.", "date": date.today() - timedelta(days=40), "contact_id": 101, "user_id": user_ids["chloe"]},
    {"type": models.ActivityType.EMAIL, "notes": "Sent over the full Project Phoenix proposal and pricing details.", "date": date.today() - timedelta(days=25), "contact_id": 101, "user_id": user_ids["chloe"]},
    {"type": models.ActivityType.MEETING, "notes": "Met with Rohan and the HealthBridge tech team. They have concerns about implementation timelines.", "date": date.today() - timedelta(days=10), "contact_id": 102, "user_id": user_ids["chloe"]},
    {"type": models.ActivityType.NOTE, "notes": "Liam noted that NextGen is also evaluating a competitor. Speed is key.", "date": date.today() - timedelta(days=5), "contact_id": 103, "user_id": user_ids["ben"]},
]

# --- Other Data (for app completeness) ---

PROJECTS_DATA = [
    {"id": 301, "name": "Q4 Product Launch: 'Odyssey'", "manager_id": user_ids["david"], "status": models.ProjectStatus.ON_TRACK, "progress": 65, "start_date": date(2025, 9, 1), "end_date": date(2025, 12, 15), "member_ids": [str(user_ids["eva"]), str(user_ids["mason"])]},
]

TASKS_DATA = [
    {"id": 401, "name": "Finalize UI/UX Mockups", "description": "Complete all Figma mockups for the Odyssey dashboard.", "status": models.TaskStatus.IN_PROGRESS, "assignee_id": user_ids["eva"], "project_id": 301, "due_date": date(2025, 10, 10)},
    {"id": 402, "name": "Setup Staging Environment API", "description": "Deploy the latest build to the staging server for QA.", "status": models.TaskStatus.TO_DO, "assignee_id": user_ids["mason"], "project_id": 301, "due_date": date(2025, 10, 15)},
]

TIMEOFF_DATA = [
    {"id": 501, "user_id": user_ids["eva"], "type": models.LeaveType.VACATION, "start_date": date(2025, 10, 20), "end_date": date(2025, 10, 24), "status": models.RequestStatus.APPROVED, "reason": "Family trip."},
]

ORGANISER_DATA = [
    {"id": "dept_sales", "parent_id": None, "type": models.OrganiserElementType.DEPARTMENT, "label": "Sales"},
    {"id": "dept_eng", "parent_id": None, "type": models.OrganiserElementType.DEPARTMENT, "label": "Engineering"},
]

def seed_database(db: Session):
    print("Clearing old data...")
    # Clear tables in reverse order of dependency to avoid foreign key constraints
    for table in reversed(models.Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()

    print("Seeding new data...")
    
    # Create the Organization
    db_org = models.Organization(**ORGANIZATION_DATA)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    org_id = db_org.id

    # Create Users
    for user_data in USERS_DATA:
        user_data["organization_id"] = org_id
        db_user = models.User(**user_data, hashed_password=get_password_hash("password123"))
        db.add(db_user)
    db.commit()

    # Create Companies
    for company_data in COMPANIES_DATA:
        company_data["organization_id"] = org_id
        db.add(models.Company(**company_data))
    db.commit()

    # Create Contacts, Deals, Tasks, etc.
    db.add_all([models.Contact(**data) for data in CONTACTS_DATA])
    db.add_all([models.Deal(**data) for data in DEALS_DATA])
    db.add_all([models.CrmTask(**data) for data in CRM_TASKS_DATA])
    db.add_all([models.Activity(**data) for data in ACTIVITIES_DATA])
    db.add_all([models.Project(**data) for data in PROJECTS_DATA])
    db.add_all([models.Task(**data) for data in TASKS_DATA])
    db.add_all([models.TimeOffRequest(**data) for data in TIMEOFF_DATA])
    
    for element_data in ORGANISER_DATA:
        element_data["organization_id"] = org_id
        db.add(models.OrganiserElement(**element_data))
    
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