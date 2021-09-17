from typing import Optional, List

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(
        title="名前",
        description="プロジェクトの名前",
        min_length=1,
        max_length=32,
        example="name example",
        nullable=False
    )
    description: Optional[str] = Field(
        title="desc",
    )

    class Config:
        schema_extra = {
            "required": {
                "name"
            }
        }


class ProjectInDBBase(ProjectBase):
    id: int = Field(
        title="id"
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "description",
                "id": 1,
            }
        }


class ProjectInDBBases(BaseModel):
    projects: List[ProjectInDBBase]


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass
