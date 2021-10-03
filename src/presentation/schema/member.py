from typing import List, Optional

from pydantic import BaseModel, Field

from src.domain.model.member import Member as MemberModel


class Member(BaseModel):
    id: Optional[int] = Field(
        title="id",
        readOnly=True,
    )
    name: str = Field(
        title="名前",
        description="メンバーの名前",
        min_length=1,
        max_length=32,
        nullable=False,
    )
    cost: int = Field(
        title="desc",
        ge=0,
        le=9999999,
        nullable=False,
    )
    cost_type: str = Field(
        title="cost type",
        description="金額のタイプ<br>1:時間<br>2:月",
        enum=["1", "2"],
        nullable=False,
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "required": {
                "name", "cost", "cost_type"
            }
        }

    @staticmethod
    def from_entity(member: MemberModel) -> "Member":
        return Member(
            id=member.id,
            name=member.name,
            cost=member.cost,
            cost_type=member.cost_type.value,
        )


class Members(BaseModel):
    members: List[Member]
