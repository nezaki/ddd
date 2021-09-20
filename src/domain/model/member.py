from pydantic import BaseModel

from src.domain.value.cost_type import CostType


class Member(BaseModel):
    name: str
    const: int
    const_type: CostType
