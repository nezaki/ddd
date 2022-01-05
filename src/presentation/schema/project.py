from typing import List, Optional

from pydantic import BaseModel, Field


class Project(BaseModel):
    id: Optional[int] = Field(
        title="id",
        readOnly=True,
    )
    name: str = Field(
        title="名前",
        description="プロジェクトの名前",
        min_length=1,
        max_length=32,
        example="name example",
        nullable=False,
    )
    description: Optional[str] = Field(
        title="desc",
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "required": {
                "name"
            }
        }


class Projects(BaseModel):
    projects: List[Project]
