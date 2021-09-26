from typing import Any, Optional

from fastapi import APIRouter, Depends, Query, Header, Response, status, Request

from src.presentation.schema.project import Project as ProjectSchema
from src.presentation.schema.project import Projects as ProjectsSchema
from src.application.service.project import ProjectService, ProjectServiceImpl
from src.domain.model.project import Project as ProjectModel


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


class CommonQueryParams:
    def __init__(
            self,
            skip: Optional[int] = Query(description="skipの説明", default=0, ge=0, le=9999999),
            limit: Optional[int] = Query(description="limitの説明", default=100, ge=1, le=1000)):
        self.skip = skip
        self.limit = limit


@router.get("", response_model=ProjectsSchema)
def read_projects(
        params: CommonQueryParams = Depends(CommonQueryParams),
        service: ProjectService = Depends(ProjectServiceImpl)):
    projects = service.read_projects(params.skip, params.limit)
    return {"projects": projects}


@router.get("/{project_id}", response_model=ProjectSchema)
def read(project_id: int, service: ProjectService = Depends(ProjectServiceImpl)) -> Any:
    project = service.read(project_id)
    return project


@router.post("", response_model=ProjectSchema)
def create(
        payload: ProjectSchema,
        service: ProjectService = Depends(ProjectServiceImpl)) -> Any:
    project = service.create(ProjectModel(**payload.dict()))
    return project


@router.put("/{project_id}", response_model=ProjectSchema)
def update(project_id: int, payload: ProjectSchema, service: ProjectService = Depends(ProjectServiceImpl)) -> Any:
    project = service.update(ProjectModel(**payload.dict()), project_id)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(project_id: int, service: ProjectService = Depends(ProjectServiceImpl)):
    service.delete(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
