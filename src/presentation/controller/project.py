from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.presentation.schema.project import ProjectInDBBase, ProjectInDBBases

from src.infrastructure.datasource.database import get_db
from src.infrastructure.datasource.repository.project import project as project_repo
from src.presentation.schema.project import ProjectCreate, ProjectUpdate


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get("/{project_id}", response_model=ProjectInDBBase, responses={status.HTTP_404_NOT_FOUND: {}})
def read(project_id: int, db: Session = Depends(get_db)):
    project = project_repo.get(db, id=project_id)
    return project


@router.get("", response_model=ProjectInDBBases)
def read_projects(db: Session = Depends(get_db)):
    projects = project_repo.get_multi(db)
    return {"projects": projects}


@router.post("", response_model=ProjectInDBBase)
async def create(*, db: Session = Depends(get_db), payload: ProjectCreate) -> Any:
    project = project_repo.create(db, obj_in=payload)
    return project


@router.put("/{project_id}", response_model=ProjectInDBBase)
def update(*, project_id: int, db: Session = Depends(get_db), payload: ProjectUpdate) -> Any:
    project = project_repo.get(db, id=project_id)
    project_updated = project_repo.update(db, db_obj=project, obj_in=payload)
    return project_updated


@router.delete("/{project_id}", status_code=204)
def delete(*, project_id: int, db: Session = Depends(get_db)) -> Any:
    project_repo.remove(db, id=project_id)
    return None
