from typing import Optional

from pydantic import BaseModel, ConfigDict


class Project(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
