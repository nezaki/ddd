from typing import List

from pydantic import BaseModel, Field


class MemberBase(BaseModel):
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


class MemberInDBBase(MemberBase):
    id: int = Field(
        title="id"
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "required": ["name", "cost", "cost_type"]
        }


class MemberInDBBases(BaseModel):
    members: List[MemberInDBBase]


class MemberCreate(MemberBase):
    pass


class MemberUpdate(MemberBase):
    pass
