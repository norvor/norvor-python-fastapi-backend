from sqlalchemy.orm import Session
from typing import List

from . import schemas
from .. import models

# --- Project CRUD Functions ---

def create_project(db: Session, project: schemas.ProjectCreate):
    """
    Create a new project.
    """
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_project(db: Session, project_id: int):
    """
    Get a single project by its ID.
    """
    return db.query(models.Project).filter(models.Project.id == project_id).first()

# --- MODIFY THIS FUNCTION ---
def get_projects(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    """
    Get a list of all projects for a specific organization.
    """
    return db.query(models.Project).join(models.User, models.Project.manager_id == models.User.id).filter(models.User.organization_id == organization_id).offset(skip).limit(limit).all()
# --------------------------


# --- Task CRUD Functions ---

def create_task(db: Session, task: schemas.TaskCreate):
    """
    Create a new task for a project.
    """
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_for_project(db: Session, project_id: int):
    """
    Get all tasks associated with a specific project.
    """
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()

# --- MODIFY THIS FUNCTION ---
def get_all_tasks(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    """
    Get a list of all tasks for a specific organization.
    """
    return db.query(models.Task).join(models.User, models.Task.assignee_id == models.User.id).filter(models.User.organization_id == organization_id).offset(skip).limit(limit).all()
# --------------------------