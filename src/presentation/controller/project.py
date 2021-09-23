from typing import Any, Optional

from fastapi import APIRouter, Depends, Query, Header

from src.presentation.schema.project import Project as ProjectSchema
from src.presentation.schema.project import Projects as ProjectsSchema
from src.application.service.project import ProjectService, ProjectServiceImpl
from src.domain.model.project import Project as ProjectModel


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


# @router.get("/{project_id}", response_model=ProjectInDBBase, responses={status.HTTP_404_NOT_FOUND: {}})
# def read(project_id: int, db: Session = Depends(get_db)):
#     project = project_repository.get(db, id=project_id)
#     return project

async def verify_token(x_token2: str = Header(...)):
    # if x_token != "fake-super-secret-token":
    #     raise HTTPException(status_code=400, detail="X-Token header invalid")
    pass


class CommonQueryParams:
    def __init__(
            self,
            skip: Optional[int] = Query(description="skipの説明", default=0, ge=0, le=9999999),
            limit: Optional[int] = Query(description="limitの説明", default=100, ge=1, le=1000)):
        self.skip = skip
        self.limit = limit


@router.get("", response_model=ProjectsSchema, dependencies=[Depends(verify_token)])
def read_projects(
        params: CommonQueryParams = Depends(CommonQueryParams),
        service: ProjectService = Depends(ProjectServiceImpl)):
    projects = service.read_projects(params.skip, params.limit)
    return {"projects": projects}


@router.post("", response_model=ProjectSchema)
def create(
        payload: ProjectSchema,
        service: ProjectService = Depends(ProjectServiceImpl)) -> Any:
    project = service.create(ProjectModel(**payload.dict()))
    return project


# @router.put("/{project_id}", response_model=ProjectInDBBase)
# def update(*, project_id: int, db: Session = Depends(get_db), payload: ProjectUpdate) -> Any:
#     project = project_repository.get(db, id=project_id)
#     project_updated = project_repository.update(db, db_obj=project, obj_in=payload)
#     return project_updated
#
#
# @router.delete("/{project_id}", status_code=204)
# def delete(*, project_id: int, db: Session = Depends(get_db)) -> Any:
#     project_repository.remove(db, id=project_id)
#     return None
