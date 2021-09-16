from src.infrastructure.datasource.entity.project import Project as ProjectEntity
from src.infrastructure.datasource.base import CRUDBase
from src.presentation.schema.project import ProjectCreate, ProjectUpdate


class Project(CRUDBase[ProjectEntity, ProjectCreate, ProjectUpdate]):
    pass


project = Project(ProjectEntity)
