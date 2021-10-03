from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infrastructure.datasource.database import get_db
from src.application.service.member import MemberService, MemberServiceImpl
from src.presentation.schema.member import Member as MemberSchema
from src.domain.model.member import Member as MemberModel


router = APIRouter(
    prefix="/members",
    tags=["Members"],
)


@router.post("", response_model=MemberSchema)
def create(payload: MemberSchema, service: MemberService = Depends(MemberServiceImpl)) -> Any:
    member = service.create(MemberModel(**payload.dict()))
    return MemberSchema.from_entity(member)
