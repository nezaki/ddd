from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship

from src.infrastructure.datasource.database import Base
from src.infrastructure.datasource._crud_base import CRUDBase
from src.infrastructure.datasource.member_allocation import MemberAllocation
from src.presentation.schema.project import ProjectCreate, ProjectUpdate


class Project(Base):
    __tablename__ = "project"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR)
    description = Column(VARCHAR)

    member_allocation = relationship("MemberAllocation", uselist=True, lazy="joined", innerjoin=False, viewonly=True)


class ProjectRepository(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    pass


project_repository = ProjectRepository(Project)
