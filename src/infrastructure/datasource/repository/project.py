from sqlalchemy.orm import Session

from src.infrastructure.datasource.entity.project import Project


def get_projects(db: Session):
    return db.query(Project).all()
