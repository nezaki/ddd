from typing import Optional

from pydantic import BaseModel

from src.domain.value.cost_type import CostType


class Member(BaseModel):
    id: Optional[int] = None
    name: str
    cost: int
    cost_type: CostType
