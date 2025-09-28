import json
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from app.auth.security import get_password_hash
from datetime import datetime, date

# --- MOCK DATA IN PYTHON FORMAT ---

USERS_DATA = [
  { "id": 1, "name": 'Alex Johnson', "role": 'Team', "avatar": 'https://picsum.photos/id/1005/200/200', "managerId": 3, "teamIds": ['bd1'], "title": 'Sales Representative', "department": 'Sales', "email": 'alex.j@norvor.com' },
  { "id": 2, "name": 'Brenda Smith', "role": 'Team', "avatar": 'https://picsum.photos/id/1011/200/200', "managerId": 3, "teamIds": ['bd1'], "title": 'Sales Representative', "department": 'Sales', "email": 'brenda.s@norvor.com' },
  { "id": 3, "name": 'Charles Brown', "role": 'Management', "avatar": 'https://picsum.photos/id/1025/200/200', "teamIds": ['bd1'], "title": 'Sales Manager', "department": 'Sales', "email": 'charles.b@norvor.com' },
  { "id": 4, "name": 'Diana Green', "role": 'Executive', "avatar": 'https://picsum.photos/id/1027/200/200', "teamIds": ['bd1', 'eng1', 'eng2'], "title": 'CEO', "department": 'Executive', "email": 'diana.g@norvor.com' },
  { "id": 5, "name": 'Ethan Hunt', "role": 'Team', "avatar": 'https://picsum.photos/id/10/200/200', "managerId": 3, "teamIds": ['eng1'], "title": 'Software Engineer', "department": 'Engineering', "email": 'ethan.h@norvor.com' },
  { "id": 6, "name": 'Fiona Glenanne', "role": 'Team', "avatar": 'https://picsum.photos/id/20/200/200', "managerId": 3, "teamIds": ['eng2'], "title": 'Software Engineer', "department": 'Engineering', "email": 'fiona.g@norvor.com' },
  { "id": 7, "name": 'George Mason', "role": 'Management', "avatar": 'https://picsum.photos/id/30/200/200', "teamIds": ['eng1', 'eng2'], "title": 'Engineering Manager', "department": 'Engineering', "email": 'george.m@norvor.com' },
]

CONTACTS_DATA = [
  { "id": 101, "name": 'InnoTech Solutions', "company": 'InnoTech', "email": 'contact@innotech.com', "phone": '555-0101', "ownerId": 1, "createdAt": '2023-10-01' },
  { "id": 102, "name": 'Quantum Dynamics', "company": 'Quantum', "email": 'info@quantum.com', "phone": '555-0102', "ownerId": 1, "createdAt": '2023-10-05' },
  { "id": 103, "name": 'Apex Innovations', "company": 'Apex', "email": 'sales@apex.com', "phone": '555-0103', "ownerId": 2, "createdAt": '2023-10-10' },
  { "id": 104, "name": 'Stellar Corp', "company": 'Stellar', "phone": '555-0104', "ownerId": 2, "createdAt": '2023-10-12', "email": 'support@stellar.com' },
  { "id": 105, "name": 'Fusion Enterprises', "company": 'Fusion', "email": 'hello@fusion.com', "phone": '555-0105', "ownerId": 5, "createdAt": '2023-10-15' },
  { "id": 106, "name": 'Zenith Systems', "company": 'Zenith', "email": 'connect@zenith.com', "phone": '555-0106', "ownerId": None, "createdAt": '2023-10-20' },
  { "id": 107, "name": 'Nova Industries', "company": 'Nova', "email": 'inquiries@nova.com', "phone": '555-0107', "ownerId": None, "createdAt": '2023-10-22' },
]

DEALS_DATA = [
  { "id": 201, "name": 'InnoTech Website Relaunch', "value": 50000, "stage": 'Proposal Sent', "contactId": 101, "ownerId": 1, "closeDate": '2024-08-30' },
  { "id": 202, "name": 'Quantum AI Integration', "value": 75000, "stage": 'Negotiation', "contactId": 102, "ownerId": 1, "closeDate": '2024-09-15' },
  { "id": 203, "name": 'Apex Cloud Migration', "value": 30000, "stage": 'Won', "contactId": 103, "ownerId": 2, "closeDate": '2024-07-20' },
  { "id": 204, "name": 'Stellar Marketing Campaign', "value": 25000, "stage": 'New Lead', "contactId": 104, "ownerId": 2, "closeDate": '2024-09-01' },
  { "id": 205, "name": 'Fusion Data Analytics', "value": 60000, "stage": 'Lost', "contactId": 105, "ownerId": 5, "closeDate": '2024-07-10' },
]

# --- SEEDING LOGIC ---

def seed_data(db: Session):
    # Clear existing data to prevent duplicates
    db.query(models.Deal).delete()
    db.query(models.Contact).delete()
    db.query(models.User).delete()
    db.commit()
    print("Cleared existing data.")

    print("Seeding users...")
    for user_data in USERS_DATA:
        db_user = models.User(
            id=user_data['id'],
            name=user_data['name'],
            email=user_data['email'],
            hashed_password="password123", # Default password for all
            role=user_data['role'],
            department=user_data['department'],
            title=user_data['title'],
            avatar=user_data['avatar']
        )
        db.add(db_user)
    db.commit()

    print("Seeding contacts...")
    for contact_data in CONTACTS_DATA:
        db_contact = models.Contact(
            id=contact_data['id'],
            name=contact_data['name'],
            company=contact_data['company'],
            email=contact_data['email'],
            phone=contact_data['phone'],
            owner_id=contact_data['ownerId'],
            created_at=datetime.strptime(contact_data['createdAt'], '%Y-%m-%d').date()
        )
        db.add(db_contact)
    db.commit()

    print("Seeding deals...")
    for deal_data in DEALS_DATA:
        db_deal = models.Deal(
            id=deal_data['id'],
            name=deal_data['name'],
            value=deal_data['value'],
            stage=deal_data['stage'],
            contact_id=deal_data['contactId'],
            owner_id=deal_data['ownerId'],
            close_date=datetime.strptime(deal_data['closeDate'], '%Y-%m-%d').date()
        )
        db.add(db_deal)
    db.commit()

    print("Seeding complete!")

if __name__ == "__main__":
    print("Starting database seeding process...")
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
        print("Database session closed.")