from typing import Any, Optional

from fastapi import APIRouter, Header

from src.presentation.schema.example import Example1, Example2


router = APIRouter(
    prefix="/example",
    tags=["Example"],
)


@router.post("")
async def multiple_body_parameters(*, example1: Example1, example2: Example2) -> Any:
    return {
        "example1": example1,
        "example2": example2,
    }


@router.get("")
async def header(user_agent: Optional[str] = Header(None)) -> Any:
    return None
