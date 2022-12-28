from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from src.domain.model.project import Project as ProjectModel
from src.infrastructure.datasource.entity.project import Project as ProjectEntity


def find(
    session: Session, skip: int | None = 0, limit: int | None = 100
) -> List[ProjectModel]:
    projects = (
        session.query(ProjectEntity)
        .order_by(ProjectEntity.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [project.to_entity() for project in projects]


def find_by_id(session: Session, project_id: int) -> ProjectModel | None:
    try:
        project: ProjectEntity = (
            session.query(ProjectEntity).filter_by(id=project_id).one()
        )
        return project.to_entity()
    except NoResultFound:
        return None
    except Exception as e:
        raise e


def create(session: Session, project: ProjectModel) -> ProjectModel:
    _project: ProjectEntity = ProjectEntity.from_entity(project)
    session.add(_project)
    session.flush()
    return _project.to_entity()


def update(session: Session, project: ProjectModel, project_id: int) -> ProjectModel:
    _project: ProjectEntity = (
        session.query(ProjectEntity).filter_by(id=project_id).one()
    )
    _project.name = project.name
    _project.description = project.description
    return _project.to_entity()


def delete(session: Session, project_id: int) -> None:
    session.query(ProjectEntity).filter_by(id=project_id).delete()
