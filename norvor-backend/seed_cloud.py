import sys
from pathlib import Path
import uuid
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta

# Add the project's root directory to the Python path.
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from app.db.session import SessionLocal
from app import models
from app.auth.security import get_password_hash

def seed_organization(db: Session, org_name: str, user_data: list, company_data: list, contact_data: list, deal_data: list):
    """
    Seeds a complete organization with all its related data.
    """
    print(f"\n--- Seeding Organization: {org_name} ---")

    # 1. Create Organization
    db_org = models.Organization(name=org_name)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    org_id = db_org.id
    print(f"Created organization '{org_name}' with ID: {org_id}")

    # 2. Create Users

    hashed_password = get_password_hash("password123")

    users = {}
    for u_data in user_data:
        user = models.User(
            id=u_data["id"],
            name=u_data["name"],
            email=u_data["email"],
            role=u_data["role"],
            title=u_data["title"],
            is_system_administrator=u_data.get("is_system_administrator", False),
            hashed_password=hashed_password, # In a real app, use get_password_hash
            organization_id=org_id
        )
        db.add(user)
        users[u_data["key"]] = user
    db.commit()
    print(f"Created {len(users)} users.")

    # 3. Create Departments and Data Buckets
    sales_dept = models.Department(name="Sales", organization_id=org_id)
    eng_dept = models.Department(name="Engineering", organization_id=org_id)
    db.add_all([sales_dept, eng_dept])
    db.commit()
    sales_bucket = models.DataBucket(department_id=sales_dept.id)
    eng_bucket = models.DataBucket(department_id=eng_dept.id)
    db.add_all([sales_bucket, eng_bucket])
    db.commit()
    print("Created Departments and Data Buckets.")

    # 4. Create Teams and Data Bowls
    sales_team = models.Team(
        name="Account Executives", 
        department_id=sales_dept.id,
        tools=[models.Tool.CRM, models.Tool.DOCS, models.Tool.REQUESTS]
    )
    eng_team = models.Team(
        name="Core Product", 
        department_id=eng_dept.id,
        tools=[models.Tool.PROJECTS, models.Tool.DOCS, models.Tool.REQUESTS]
    )
    db.add_all([sales_team, eng_team])
    db.commit()
    sales_bowl = models.DataBowl(team_id=sales_team.id, data_bucket_id=sales_bucket.id)
    eng_bowl = models.DataBowl(team_id=eng_team.id, data_bucket_id=eng_bucket.id)
    db.add_all([sales_bowl, eng_bowl])
    db.commit()
    print("Created Teams and Data Bowls.")

    # 5. Create Team Roles and Data Cups
    team_roles = {}
    for key, user in users.items():
        team = sales_team if "sales" in key else eng_team
        bowl = sales_bowl if "sales" in key else eng_bowl
        role_name = "Manager" if "manager" in key else "Member"
        
        team_role = models.TeamRole(user_id=user.id, team_id=team.id, role=role_name)
        db.add(team_role)
        db.commit()
        
        data_cup = models.DataCup(data_bowl_id=bowl.id, team_role_id=team_role.id)
        db.add(data_cup)
        db.commit()
        team_roles[key] = {"role": team_role, "cup": data_cup}
    print("Created Team Roles and Data Cups.")

    # 6. Create Companies
    companies = {}
    for c_data in company_data:
        company = models.Company(name=c_data["name"], domain=c_data["domain"], organization_id=org_id)
        db.add(company)
        db.commit()
        companies[c_data["id"]] = company
    print(f"Created {len(companies)} companies.")

    # 7. Create Contacts
    contacts = {}
    for ct_data in contact_data:
        owner_role = team_roles[ct_data["owner_key"]]
        contact = models.Contact(
            name=ct_data["name"],
            email=ct_data["email"],
            company_id=companies[ct_data["company_id"]].id,
            owner_id=owner_role["role"].user_id,
            data_cup_id=owner_role["cup"].id,
            created_at=date.today()
        )
        db.add(contact)
        db.commit()
        contacts[ct_data["id"]] = contact
    print(f"Created {len(contacts)} contacts.")
    
    # 8. Create Deals
    for d_data in deal_data:
        owner_role = team_roles[d_data["owner_key"]]
        deal = models.Deal(
            name=d_data["name"],
            value=d_data["value"],
            stage=d_data["stage"],
            company_id=companies[d_data["company_id"]].id,
            contact_id=contacts[d_data["contact_id"]].id,
            owner_id=owner_role["role"].user_id,
            data_cup_id=owner_role["cup"].id,
            close_date=date.today() + timedelta(days=30)
        )
        db.add(deal)
    db.commit()
    print(f"Created {len(deal_data)} deals.")

def main():
    print("--- Starting Database Seeding ---")
    db = SessionLocal()

    # Clear old data
    print("Clearing old data...")
    for table in reversed(models.Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()

    # --- ORGANIZATION 1: QuantumLeap Dynamics ---
    quantum_users = [
        {"id": uuid.uuid4(), "key": "exec", "name": "Anya Sharma", "email": "anya.sharma@quantumleap.dev", "role": models.UserRole.EXECUTIVE, "title": "CEO", "is_system_administrator": True},
        {"id": uuid.uuid4(), "key": "sales_manager", "name": "Ben Carter", "email": "ben.carter@quantumleap.dev", "role": models.UserRole.MANAGEMENT, "title": "VP of Sales"},
        {"id": uuid.uuid4(), "key": "sales_rep1", "name": "Chloe Davis", "email": "chloe.davis@quantumleap.dev", "role": models.UserRole.TEAM, "title": "Account Executive"},
        {"id": uuid.uuid4(), "key": "eng_manager", "name": "David Rodriguez", "email": "david.r@quantumleap.dev", "role": models.UserRole.MANAGEMENT, "title": "Engineering Lead"},
        {"id": uuid.uuid4(), "key": "eng_dev1", "name": "Eva Martinez", "email": "eva.martinez@quantumleap.dev", "role": models.UserRole.TEAM, "title": "Senior Developer"},
    ]
    quantum_companies = [
        {"id": 1, "name": "Fintech Innovators Inc.", "domain": "fintechinnovate.com"},
        {"id": 2, "name": "HealthBridge Solutions", "domain": "healthbridge.io"},
    ]
    quantum_contacts = [
        {"id": 101, "name": "Priya Singh", "email": "priya.singh@fintechinnovate.com", "company_id": 1, "owner_key": "sales_rep1"},
        {"id": 102, "name": "Rohan Mehta", "email": "rohan.mehta@healthbridge.io", "company_id": 2, "owner_key": "sales_rep1"},
    ]
    quantum_deals = [
        {"name": "Project Phoenix - Platform Overhaul", "value": 250000.00, "stage": models.DealStage.NEGOTIATION, "company_id": 1, "contact_id": 101, "owner_key": "sales_rep1"},
        {"name": "Patient Data API Integration", "value": 120000.00, "stage": models.DealStage.PROPOSAL_SENT, "company_id": 2, "contact_id": 102, "owner_key": "sales_rep1"},
    ]
    seed_organization(db, "QuantumLeap Dynamics", quantum_users, quantum_companies, quantum_contacts, quantum_deals)

    # --- ORGANIZATION 2: Stellar Solutions ---
    stellar_users = [
        {"id": uuid.uuid4(), "key": "exec", "name": "Ken Thompson", "email": "ken.t@stellar.io", "role": models.UserRole.EXECUTIVE, "title": "President", "is_system_administrator": True},
        {"id": uuid.uuid4(), "key": "sales_manager", "name": "Laura Chen", "email": "laura.c@stellar.io", "role": models.UserRole.MANAGEMENT, "title": "Sales Director"},
        {"id": uuid.uuid4(), "key": "sales_rep1", "name": "Michael Brown", "email": "michael.b@stellar.io", "role": models.UserRole.TEAM, "title": "Sales Associate"},
        {"id": uuid.uuid4(), "key": "eng_manager", "name": "Sofia Garcia", "email": "sofia.g@stellar.io", "role": models.UserRole.MANAGEMENT, "title": "Head of Engineering"},
    ]
    stellar_companies = [
        {"id": 3, "name": "Aperture Labs", "domain": "aperture.com"},
        {"id": 4, "name": "Black Mesa", "domain": "blackmesa.com"},
    ]
    stellar_contacts = [
        {"id": 103, "name": "Cave Johnson", "email": "cave.j@aperture.com", "company_id": 3, "owner_key": "sales_rep1"},
        {"id": 104, "name": "Wallace Breen", "email": "wallace.b@blackmesa.com", "company_id": 4, "owner_key": "sales_rep1"},
    ]
    stellar_deals = [
        {"name": "Portal Gun Contract", "value": 1500000.00, "stage": models.DealStage.WON, "company_id": 3, "contact_id": 103, "owner_key": "sales_rep1"},
        {"name": "HEV Suit Procurement", "value": 750000.00, "stage": models.DealStage.NEW_LEAD, "company_id": 4, "contact_id": 104, "owner_key": "sales_rep1"},
    ]
    seed_organization(db, "Stellar Solutions", stellar_users, stellar_companies, stellar_contacts, stellar_deals)

    print("\n✅ Database seeding complete!")
    print("You can log in with any user's email (e.g., 'anya.sharma@quantumleap.dev' or 'ken.t@stellar.io').")
    print("The password for all users is: password123")
    
    db.close()

if __name__ == "__main__":
    main()