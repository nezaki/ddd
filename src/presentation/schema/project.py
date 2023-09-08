from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from src.domain.model.project import Project as ProjectModel


class Project(BaseModel):
    id: int | None = Field(
        default=None,
        title="id",
    )
    name: str = Field(
        title="名前",
        description="名前",
        min_length=1,
        max_length=32,
    )
    description: str | None = Field(
        default=None,
        title="説明",
        description="説明",
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
