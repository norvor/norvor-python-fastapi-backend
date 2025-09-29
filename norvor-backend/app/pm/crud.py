from sqlalchemy.orm import Session
from typing import List

from . import schemas
from .. import models

# --- Project CRUD Functions ---

def create_project(db: Session, project: schemas.ProjectCreate):
    """
    Create a new project.
    """
    # Note: In a real app, you'd handle adding members via a separate table/process.
    # For now, we're just storing the IDs.
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

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of all projects.
    """
    return db.query(models.Project).offset(skip).limit(limit).all()


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

def get_all_tasks(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of all tasks.
    """
    return db.query(models.Task).offset(skip).limit(limit).all()