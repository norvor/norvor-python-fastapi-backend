from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Enum,
    Date,
    ForeignKey,
    JSON,
    Text,
    DateTime, # Import DateTime for timestamps
)
from sqlalchemy.orm import relationship, declarative_base
import enum
from datetime import datetime
from ..db.base import Base 


# --- User Model ---
class UserRole(str, enum.Enum):
    TEAM = "Team"
    MANAGEMENT = "Management"
    EXECUTIVE = "Executive"

# ADD THE NEW ORGANIZATION CLASS
class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    users = relationship("User", back_populates="organization")

# UPDATE THE USER CLASS
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # --- ADD THESE TWO LINES ---
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization", back_populates="users")
    # -------------------------
    role = Column(Enum(UserRole))
    avatar = Column(String, nullable=True)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String, nullable=True)
    department = Column(String)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    emergency_contact = Column(String, nullable=True)
    leave_balance = Column(JSON, nullable=True)

    manager = relationship("User", remote_side=[id])
    projects = relationship("Project", back_populates="manager")

# --- CRM Models ---
class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    company = Column(String)
    email = Column(String, index=True)
    phone = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
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

# --- Project Management Models ---
class ProjectStatus(str, enum.Enum):
    ON_TRACK = 'On Track'
    AT_RISK = 'At Risk'
    OFF_TRACK = 'Off Track'
    COMPLETED = 'Completed'

class TaskStatus(str, enum.Enum):
    TO_DO = 'To Do'
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    manager_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(ProjectStatus))
    progress = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    member_ids = Column(JSON, default=[])
    manager = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus))
    assignee_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    due_date = Column(Date)
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User")

# --- HR Models ---
class LeaveType(str, enum.Enum):
    VACATION = 'Vacation'
    SICK = 'Sick Leave'
    PERSONAL = 'Personal Day'

class RequestStatus(str, enum.Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    DENIED = 'Denied'

class TimeOffRequest(Base):
    __tablename__ = "time_off_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Enum(LeaveType))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum(RequestStatus))
    reason = Column(String, nullable=True)
    user = relationship("User")

# --- Organiser Models ---
class OrganiserElementType(str, enum.Enum):
    DEPARTMENT = 'Department'
    TEAM = 'Team'
    ROLE = 'Role'
    SOFTWARE = 'Software'
    PROCESS = 'Process Step'

class OrganiserElement(Base):
    __tablename__ = "organiser_elements"
    id = Column(String, primary_key=True, index=True)
    parent_id = Column(String, ForeignKey("organiser_elements.id"), nullable=True)
    type = Column(Enum(OrganiserElementType))
    label = Column(String)
    properties = Column(JSON, default={})
    parent = relationship("OrganiserElement", remote_side=[id], back_populates="children")
    children = relationship("OrganiserElement", back_populates="parent")

# --- Docs Model ---
class Doc(Base):
    __tablename__ = "docs"
    id = Column(String, primary_key=True, index=True)
    parent_id = Column(String, ForeignKey("docs.id"), nullable=True)
    title = Column(String)
    icon = Column(String, nullable=True, default="📄")
    content = Column(Text, nullable=True, default="")
    parent = relationship("Doc", remote_side=[id], back_populates="children")
    children = relationship("Doc", back_populates="parent")

# --- ADD EVERYTHING BELOW THIS LINE ---

# --- Requests (Ticket) Enums and Models ---
class TicketStatus(str, enum.Enum):
    OPEN = 'Open'
    IN_PROGRESS = 'In Progress'
    CLOSED = 'Closed'

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN)
    submitted_by = Column(Integer, ForeignKey("users.id"))
    team_id = Column(String) # This could link to an OrganiserElement of type TEAM
    created_at = Column(DateTime, default=datetime.utcnow)
    
    submitter = relationship("User")