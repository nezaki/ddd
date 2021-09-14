from typing import Optional

from pydantic import BaseModel, Field


class Project(BaseModel):
    id: int = Field(
        title="id"
    )
    name: str = Field(
        title="名前",
        description="プロジェクトの名前",
        min_length=1,
        max_length=128,
        example="name example",
        nullable=True
    )
    description: Optional[str] = Field(
        title="desc",
    )

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "name example",
                "description": "description example",
            },
            "required": {
                "name"
            }
        }
        orm_mode = True
