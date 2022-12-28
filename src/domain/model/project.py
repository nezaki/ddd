from typing import Optional

from pydantic import BaseModel


class Project(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True
