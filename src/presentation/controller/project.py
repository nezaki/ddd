from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.presentation.model.project import Project
from src.infrastructure.datasource.database import get_db
from src.infrastructure.datasource.repository.project import get_projects


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get("", response_model=Project)
async def findall(db: Session = Depends(get_db)):
    projects = get_projects(db)
    return projects[0]
