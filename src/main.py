import logging
import time
from datetime import datetime
from typing import Callable, Dict

import uvicorn
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from fastapi import Depends, FastAPI, Header, Request
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from src.config import get_settings
from src.presentation.controller.example import router as example_router
from src.presentation.controller.project import router as project_router

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger("sqlalchemy.engine").setLevel(level=logging.DEBUG)


async def verify_token(x_token: str = Header(...)) -> None:
    pass


space = "  "
description = f"""
api{space}
description{space}
[リンクサンプル](https://google.com){space}
"""

app = FastAPI(
    debug=True,
    title="api title",
    description=description,
    version="0.0.1",
    root_path="",
    dependencies=[Depends(verify_token)],
    docs_url="/docs",
    redoc_url="/redoc",
)
app.include_router(project_router)
app.include_router(example_router)


@app.on_event("startup")
async def startup() -> None:
    logger.debug("startup")


@app.on_event("shutdown")
async def shutdown() -> None:
    logger.debug("shutdown")


@app.middleware("http")
async def process_time(request: Request, call_next: Callable):  # noqa
    path = request.url.path
    method = request.method
    start = time.perf_counter()
    start_datetime = datetime.now().isoformat()

    logger.debug(f"{start_datetime} {method} {path}: start")

    response = await call_next(request)

    end = time.perf_counter()
    end_datetime = datetime.now().isoformat()
    logger.debug(f"{end_datetime} {method} {path}: end {end - start} sec")

    return response


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> Response:
    logger.debug("StarletteHTTPException")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> Response:
    logger.debug("RequestValidationError")
    return await request_validation_exception_handler(request, exc)


if get_settings().BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in get_settings().BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        timeout_keep_alive=30,
        log_level=logging.DEBUG,
    )
