from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Enum,
    Date,
    ForeignKey,
    JSON,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    TEAM = "Team"
    MANAGEMENT = "Management"
    EXECUTIVE = "Executive"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(Enum(UserRole))
    avatar = Column(String)
    manager_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    department = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(String)
    emergency_contact = Column(String)
    leave_balance = Column(JSON)

    manager = relationship("User", remote_side=[id])


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    company = Column(String)
    email = Column(String, index=True)
    phone = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(Date)

    owner = relationship("User")


class DealStage(str, enum.Enum):
    NEW_LEAD = "New Lead"
    PROPOSAL_SENT = "Proposal Sent"
    NEGOTIATION = "Negotiation"
    WON = "Won"
    LOST = "Lost"


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(Float)
    stage = Column(Enum(DealStage))
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    close_date = Column(Date)

    contact = relationship("Contact")
    owner = relationship("User")