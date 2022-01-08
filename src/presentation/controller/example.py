import logging
from time import sleep
from typing import Any, NoReturn, Optional

from fastapi import APIRouter, BackgroundTasks, Header, Request, Response
from fastapi.responses import JSONResponse
from src.presentation.schema.example import Example1, Example2

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
async def header(response: Response, user_agent: Optional[str] = Header(None)) -> Any:
    response.headers["test-header"] = "test"
    return None


@router.get("/response-direct")
async def response_directly() -> Any:
    content = {"message": "Hello World"}
    headers = {"X-Cat-Dog": "alone in the world"}
    return JSONResponse(content=content, headers=headers)


@router.get("/request-direct")
async def request_directly(request: Request) -> Any:
    return JSONResponse(content={
        "url": request.url.path,
        "method": request.method,
    })


async def _task() -> NoReturn:
    for i in range(10):
        sleep(1)
        logger.debug(f"{i}")
    logger.debug("background task finish")


@router.get("/background-tasks")
async def background_tasks(background_tasks: BackgroundTasks) -> Any:
    background_tasks.add_task(_task)
    return None
