from fastapi import APIRouter, Depends, HTTPException, Response, status
from src.application.service.project import ProjectService, ProjectServiceImpl
from src.domain.model.project import Project as ProjectModel
from src.presentation.controller._common_query_param import CommonQueryParams
from src.presentation.schema.project import Project as ProjectSchema
from src.presentation.schema.project import ProjectPatch as ProjectPatchSchema
from src.presentation.schema.project import Projects as ProjectsSchema

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    dependencies=None,
    on_startup=None,
    on_shutdown=None,
    deprecated=False,
)


@router.get(
    path="",
    name="get_projects name",
    summary="get_projects summary",
    description="get_projects description",
    response_description="get_projects response_description",
    status_code=status.HTTP_200_OK,
    response_model=ProjectsSchema,
    response_model_exclude=None,
    response_model_exclude_none=False,
    dependencies=None,
    include_in_schema=True,
    deprecated=False,
)
async def get_projects(
    params: CommonQueryParams = Depends(CommonQueryParams),
    service: ProjectService = Depends(ProjectServiceImpl),
) -> ProjectsSchema:
    projects = await service.read_projects(params.skip, params.limit)
    return ProjectsSchema(projects=projects)  # type: ignore


@router.get("/{project_id}", response_model=ProjectSchema)
async def get_project(
    project_id: int, service: ProjectService = Depends(ProjectServiceImpl)
) -> ProjectSchema | None:
    project = await service.read(project_id)
    if project is None:
        raise HTTPException(status_code=404)
    return ProjectSchema.from_entity(project)


@router.post("", response_model=ProjectSchema)
async def post(
    payload: ProjectSchema, service: ProjectService = Depends(ProjectServiceImpl)
) -> ProjectSchema:
    project = await service.create(ProjectModel(**payload.dict()))
    return ProjectSchema.from_entity(project)


@router.put("/{project_id}", response_model=ProjectSchema)
async def put(
    project_id: int,
    payload: ProjectSchema,
    service: ProjectService = Depends(ProjectServiceImpl),
) -> ProjectSchema:
    project = await service.replace(ProjectModel(**payload.dict()), project_id)
    return ProjectSchema.from_entity(project)


@router.patch("/{project_id}", response_model=ProjectPatchSchema)
async def patch(
    project_id: int,
    payload: ProjectPatchSchema,
    service: ProjectService = Depends(ProjectServiceImpl),
) -> ProjectSchema:
    project = await service.update(payload.dict(exclude_unset=True), project_id)
    return ProjectSchema.from_entity(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    project_id: int, service: ProjectService = Depends(ProjectServiceImpl)
) -> Response:
    await service.delete(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
