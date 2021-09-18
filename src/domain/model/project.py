from typing import Optional

from pydantic import BaseModel


class Project(BaseModel):
    id: int
    name: str
    description: Optional[str]
