from typing import Optional

from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.schema import Column

from src.domain.model.project import Project as ProjectModel
from src.infrastructure.datasource.database import Base


class Project(Base):
    __tablename__ = "project"

    id: int = Column(INTEGER, primary_key=True)
    name: str = Column(VARCHAR)
    description: Optional[str] = Column(VARCHAR)

    def to_model(self) -> ProjectModel:
        return ProjectModel(
            id=self.id,  # type: ignore
            name=self.name,
            description=self.description,
        )

    @staticmethod
    def from_model(project: ProjectModel) -> "Project":
        return Project(
            id=project.id,  # type: ignore
            name=project.name,
            description=project.description
        )
