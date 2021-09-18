from typing import Any

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from src.infrastructure.datasource.database import get_db
from src.infrastructure.datasource.member import member_repository
from src.presentation.schema.member import MemberInDBBase, MemberCreate, MemberUpdate


router = APIRouter(
    prefix="/members",
    tags=["Members"],
)


# @router.get("/{project_id}", response_model=ProjectInDBBase, responses={status.HTTP_404_NOT_FOUND: {}})
# def read(project_id: int, db: Session = Depends(get_db)):
#     project = project_repository.get(db, id=project_id)
#     return project
#
#
# @router.get("", response_model=ProjectInDBBases)
# def read_projects(
#         skip: int = Query(description="skipの説明", default=0, ge=0),
#         limit: int = Query(default=100, le=100),
#         db: Session = Depends(get_db)):
#     projects = project_repository.get_multi(db, skip=skip, limit=limit)
#     return {"projects": projects}


@router.post("", response_model=MemberInDBBase)
def create(*, db: Session = Depends(get_db), payload: MemberCreate) -> Any:
    member = member_repository.create(db, obj_in=payload)
    return member


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
