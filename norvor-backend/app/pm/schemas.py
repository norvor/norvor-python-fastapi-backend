from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from ..models import ProjectStatus, TaskStatus # Importing Enums from models.py

# --- Task Schemas ---

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    due_date: date
    status: TaskStatus

class TaskCreate(TaskBase):
    assignee_id: int
    project_id: int

class Task(TaskBase):
    id: int
    assignee_id: int
    project_id: int

    class Config:
        from_attributes = True


# --- Project Schemas ---

class ProjectBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    status: ProjectStatus
    progress: int

class ProjectCreate(ProjectBase):
    manager_id: int
    member_ids: List[int] = []

class Project(ProjectBase):
    id: int
    manager_id: int
    tasks: List[Task] = [] # We can show related tasks when fetching a project
    member_ids: List[int] = [] # Storing member IDs as a simple list for now

    class Config:
        from_attributes = True