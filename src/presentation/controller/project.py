from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field
from starlette.requests import Request


class Project(BaseModel):
    name: str = Field(
        default=None,
        title="名前",
        description="プロジェクトの名前",
        min_length="1",
        max_length="128",
        example="name example",
        nullable=True)
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "name example",
                "description": "description example",
            },
            "required": {
                "name"
            }
        }


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get("", response_model=Project)
async def projects_findall(request: Request):
    return {"name": "テスト"}
