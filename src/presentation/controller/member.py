from fastapi import APIRouter, Depends
from src.application.service.member import MemberService, MemberServiceImpl
from src.domain.model.member import Member as MemberModel
from src.presentation.schema.member import Member as MemberSchema

router = APIRouter(
    prefix="/members",
    tags=["Members"],
)


@router.post("", response_model=MemberSchema)
def create(
    payload: MemberSchema, service: MemberService = Depends(MemberServiceImpl)
) -> MemberSchema:
    member = service.create(MemberModel(**payload.dict()))
    return MemberSchema.from_entity(member)
