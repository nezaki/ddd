from enum import Enum
from typing import List, Type, TypeVar

T = TypeVar("T", bound="EnumBase")


class EnumBase(Enum):
    def __new__(cls: Type[T], value: str, description: str = ""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def all(cls: Type[T]) -> List[str]:
        return [c.value for c in list(cls.__members__.values())]

    @classmethod
    def all_description(cls: Type[T]) -> str:
        list_ = [f"{c.value}: {c.description}" for c in list(cls.__members__.values())]
        return "<br>".join(list_)
