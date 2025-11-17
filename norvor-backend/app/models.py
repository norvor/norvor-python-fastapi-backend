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
    DateTime,
    Boolean
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime
from .db.base_class import Base

# --- ENUMS ---
class UserRole(str, enum.Enum):
    TEAM = "Team"
    MANAGEMENT = "Management"
    EXECUTIVE = "Executive"

class DealStage(str, enum.Enum):
    NEW_LEAD = "New Lead"
    PROPOSAL_SENT = "Proposal Sent"
    NEGOTIATION = "Negotiation"
    WON = "Won"
    LOST = "Lost"

class ProjectStatus(str, enum.Enum):
    ON_TRACK = 'On Track'
    AT_RISK = 'At Risk'
    OFF_TRACK = 'Off Track'
    COMPLETED = 'Completed'

class TaskStatus(str, enum.Enum):
    TO_DO = 'To Do'
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'

class CrmTaskStatus(str, enum.Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class LeaveType(str, enum.Enum):
    VACATION = 'Vacation'
    SICK = 'Sick Leave'
    PERSONAL = 'Personal Day'

class RequestStatus(str, enum.Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    DENIED = 'Denied'

class ActivityType(str, enum.Enum):
    CALL = 'Call'
    EMAIL = 'Email'
    MEETING = 'Meeting'
    NOTE = 'Note'

class TicketStatus(str, enum.Enum):
    OPEN = 'Open'
    IN_PROGRESS = 'In Progress'
    CLOSED = 'Closed'

class Tool(str, enum.Enum):
    CRM = "crm"
    PROJECTS = "pm"
    DOCS = "docs"
    HR = "hr"
    REQUESTS = "requests"
    DATALABS = "datalabs"

# --- Models ---

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    has_completed_onboarding = Column(Boolean, default=False)
    
    users = relationship("User", back_populates="organization")
    companies = relationship("Company", back_populates="organization")
    departments = relationship("Department", back_populates="organization")

class Department(Base):
    __tablename__ = "departments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    immutable = Column(Boolean, default=False)
    
    organization = relationship("Organization", back_populates="departments")
    teams = relationship("Team", back_populates="department")
    data_bucket = relationship("DataBucket", uselist=False, back_populates="department") 

class DataBucket(Base):
    __tablename__ = "data_buckets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    
    department = relationship("Department", back_populates="data_bucket")
    data_bowls = relationship("DataBowl", back_populates="data_bucket")

class Team(Base):
    __tablename__ = "teams"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    immutable = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    team_leader_id = Column(UUID(as_uuid=True), ForeignKey("team_roles.id"), nullable=True)
    tools = Column(ARRAY(Enum(Tool)), default=[])
    
    department = relationship("Department", back_populates="teams")
    team_roles = relationship("TeamRole", back_populates="team", foreign_keys="[TeamRole.team_id]")
    data_bowl = relationship("DataBowl", uselist=False, back_populates="team")
    team_leader = relationship("TeamRole", foreign_keys=[team_leader_id])

class DataBowl(Base):
    __tablename__ = "data_bowls"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"))
    data_bucket_id = Column(UUID(as_uuid=True), ForeignKey("data_buckets.id"))
    master_owner_team = Column(UUID(as_uuid=True))

    team = relationship("Team", back_populates="data_bowl")
    data_bucket = relationship("DataBucket", back_populates="data_bowls")
    data_cups = relationship("DataCup", back_populates="data_bowl")

class TeamRole(Base):
    __tablename__ = "team_roles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"))
    role = Column(String, default="Member")
    
    user = relationship("User", back_populates="team_roles")
    team = relationship("Team", back_populates="team_roles", foreign_keys=[team_id])
    data_cup = relationship("DataCup", uselist=False, back_populates="team_role")

class DataCup(Base):
    __tablename__ = "data_cups"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_bowl_id = Column(UUID(as_uuid=True), ForeignKey("data_bowls.id"))
    team_role_id = Column(UUID(as_uuid=True), ForeignKey("team_roles.id"), nullable=True)
    
    data_bowl = relationship("DataBowl", back_populates="data_cups")
    team_role = relationship("TeamRole", back_populates="data_cup")
    deals = relationship("Deal", back_populates="data_cup")
    docs = relationship("Doc", back_populates="data_cup")
    projects = relationship("Project", back_populates="data_cup")
    contacts = relationship("Contact", back_populates="data_cup")

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(255))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    role = Column(Enum(UserRole))
    is_system_administrator = Column(Boolean, default=False)
    avatar = Column(String, nullable=True)
    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    title = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    emergency_contact = Column(String, nullable=True)
    leave_balance = Column(JSON, nullable=True)
    # --- ADD THIS LINE ---
    department = Column(String, nullable=True)
    # --------------------

    organization = relationship("Organization", back_populates="users")
    manager = relationship("User", remote_side=[id], backref="direct_reports")
    team_roles = relationship("TeamRole", back_populates="user")
    
    projects = relationship("Project", back_populates="manager")
    assigned_tasks = relationship("Task", back_populates="assignee")
    time_off_requests = relationship("TimeOffRequest", back_populates="user")
    submitted_tickets = relationship("Ticket", back_populates="submitter")
    
    owned_contacts = relationship("Contact", back_populates="owner")
    owned_deals = relationship("Deal", back_populates="owner")
    owned_crm_tasks = relationship("CrmTask", back_populates="owner")
    logged_activities = relationship("Activity", back_populates="user")


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    domain = Column(String, nullable=True, unique=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    
    organization = relationship("Organization", back_populates="companies")
    contacts = relationship("Contact", back_populates="company")
    deals = relationship("Deal", back_populates="company")


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    email = Column(String, index=True)
    phone = Column(String, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(Date)
    data_cup_id = Column(UUID(as_uuid=True), ForeignKey("data_cups.id"))
    
    owner = relationship("User", back_populates="owned_contacts")
    company = relationship("Company", back_populates="contacts")
    deals = relationship("Deal", back_populates="contact")
    activities = relationship("Activity", back_populates="contact")
    crm_tasks = relationship("CrmTask", back_populates="contact")
    data_cup = relationship("DataCup", back_populates="contacts")

class Deal(Base):
    __tablename__ = "deals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(Float)
    stage = Column(Enum(DealStage))
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    close_date = Column(Date)
    data_cup_id = Column(UUID(as_uuid=True), ForeignKey("data_cups.id"))

    company = relationship("Company", back_populates="deals")
    contact = relationship("Contact", back_populates="deals")
    owner = relationship("User", back_populates="owned_deals")
    crm_tasks = relationship("CrmTask", back_populates="deal")
    data_cup = relationship("DataCup", back_populates="deals")

class CrmTask(Base):
    __tablename__ = "crm_tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    due_date = Column(DateTime)
    status = Column(Enum(CrmTaskStatus), default=CrmTaskStatus.NOT_STARTED)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=True)

    owner = relationship("User", back_populates="owned_crm_tasks")
    contact = relationship("Contact", back_populates="crm_tasks")
    deal = relationship("Deal", back_populates="crm_tasks")

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(ActivityType))
    notes = Column(Text, nullable=True)
    date = Column(Date)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    contact = relationship("Contact", back_populates="activities")
    user = relationship("User", back_populates="logged_activities")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status = Column(Enum(ProjectStatus))
    progress = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    member_ids = Column(JSON, default=[])
    data_cup_id = Column(UUID(as_uuid=True), ForeignKey("data_cups.id"))
    
    manager = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    data_cup = relationship("DataCup", back_populates="projects")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus))
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    due_date = Column(Date)
    
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks")

class TimeOffRequest(Base):
    __tablename__ = "time_off_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    type = Column(Enum(LeaveType))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum(RequestStatus))
    reason = Column(String, nullable=True)
    
    user = relationship("User", back_populates="time_off_requests")

class Doc(Base):
    __tablename__ = "docs"
    id = Column(String, primary_key=True, index=True)
    parent_id = Column(String, ForeignKey("docs.id"), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    title = Column(String)
    icon = Column(String, nullable=True, default="📄")
    content = Column(Text, nullable=True, default="")
    data_cup_id = Column(UUID(as_uuid=True), ForeignKey("data_cups.id"))
    
    parent = relationship("Doc", remote_side=[id], back_populates="children")
    children = relationship("Doc", back_populates="parent")
    data_cup = relationship("DataCup", back_populates="docs")


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN)
    submitted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    team_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    submitter = relationship("User", back_populates="submitted_tickets")
