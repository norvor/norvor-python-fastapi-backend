from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from . import crud, schemas
from ..db.session import get_db
from ..users.crud import get_user
from ..users.crud import get_user_datacups
from ..auth.security import get_current_user
from .. import models

router = APIRouter()

# --- Project Endpoints ---

@router.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    """
    Create a new project.
    """
    db_manager = get_user(db, user_id=project.manager_id)
    if not db_manager:
        raise HTTPException(status_code=404, detail=f"Manager with id {project.manager_id} not found")

    return crud.create_project(db=db, project=project)

@router.get("/projects/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Retrieve all projects for the current user's organization.
    """
    projects = crud.get_projects(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return projects

@router.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single project by its ID.
    """
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

# --- Task Endpoints ---

@router.get("/my_projects/", response_model=List[schemas.Project])
def read_my_projects(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Retrieve all projects for the current user from all their DataCups using an optimized query.
    """
    return crud.get_projects_for_user(db, user_id=current_user.id)

@router.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task for a project.
    """
    db_project = crud.get_project(db, project_id=task.project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail=f"Project with id {task.project_id} not found")

    db_assignee = get_user(db, user_id=task.assignee_id)
    if not db_assignee:
        raise HTTPException(status_code=404, detail=f"Assignee with id {task.assignee_id} not found")

    return crud.create_task(db=db, task=task)



@router.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Retrieve all tasks for the current user's organization.
    """
    tasks = crud.get_all_tasks(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return tasks