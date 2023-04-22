from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.schema import Column

from src.domain.model.project import Project as ProjectModel
from src.infrastructure.datasource.database import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR)
    description = Column(VARCHAR)

    def to_model(self) -> ProjectModel:
        return ProjectModel(id=self.id, name=self.name, description=self.description)  # type: ignore

    @staticmethod
    def from_model(project: ProjectModel) -> "Project":
        return Project(
            id=project.id, name=project.name, description=project.description
        )
