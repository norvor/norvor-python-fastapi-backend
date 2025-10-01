from sqlalchemy.orm import Session
from typing import List

from . import schemas
from .. import models
from uuid import UUID

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

def get_projects_by_data_cup_ids(db: Session, data_cup_ids: List[UUID]):
    """
    Get all projects from a list of DataCup IDs.
    """
    return db.query(models.Project).filter(models.Project.data_cup_id.in_(data_cup_ids)).all()

def get_projects_for_user(db: Session, user_id: UUID):
    """
    Get all projects for a user in a single, optimized query using JOINs.
    """
    return db.query(models.Project).join(models.DataCup).join(models.TeamRole).filter(models.TeamRole.user_id == user_id).all()


def get_tasks_for_project(db: Session, project_id: int):
    """
    Get all tasks associated with a specific project.
    """
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()
# In get_projects function:
def get_projects(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Project).join(models.User, models.Project.manager_id == models.User.id).filter(models.User.organization_id == organization_id).offset(skip).limit(limit).all()

# In get_all_tasks function:
def get_all_tasks(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Task).join(models.User, models.Task.assignee_id == models.User.id).filter(models.User.organization_id == organization_id).offset(skip).limit(limit).all()