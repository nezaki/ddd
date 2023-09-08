from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from src.domain.model.project import Project as ProjectModel


class Project(BaseModel):
    id: int | None = Field(
        default=None,
        title="id-title",
        json_schema_extra={
            "readOnly": True,
        }
    )
    name: str = Field(
        title="name-title",
        description="name-description",
        min_length=1,
        max_length=32,
    )
    description: str | None = Field(
        default=None,
        title="description-title",
        description="description-description",
        min_length=1,
        max_length=256,
    )
    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_entity(project: ProjectModel) -> "Project":
        return Project(
            id=project.id,
            name=project.name,
            description=project.description,
        )


class Projects(BaseModel):
    projects: List[Project]


class ProjectPatch(Project):
    name: Optional[str] = Project.model_fields.get("name")  # type: ignore
