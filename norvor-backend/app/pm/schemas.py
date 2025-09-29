from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from uuid import UUID # --- ADD THIS IMPORT ---
from ..models import ProjectStatus, TaskStatus 

# --- Task Schemas ---

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    due_date: date
    status: TaskStatus

class TaskCreate(TaskBase):
    # --- MODIFY THIS LINE ---
    assignee_id: UUID
    # ----------------------
    project_id: int

class Task(TaskBase):
    id: int
    # --- MODIFY THIS LINE ---
    assignee_id: UUID
    # ----------------------
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
    # --- MODIFY THIS LINE ---
    manager_id: UUID
    member_ids: List[UUID] = []
    # ----------------------

class Project(ProjectBase):
    id: int
    # --- MODIFY THIS LINE ---
    manager_id: UUID
    member_ids: List[UUID] = []
    # ----------------------
    tasks: List[Task] = [] 

    class Config:
        from_attributes = True