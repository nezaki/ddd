import logging
import time
import uvicorn

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from src.presentation.controller.project import router as project_router
from src.presentation.controller.member import router as member_router
from src.presentation.controller.example import router as example_router
from src.config import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(project_router)
app.include_router(member_router)
app.include_router(example_router)


@app.on_event("startup")
async def startup():
    logger.debug("startup")


@app.on_event("shutdown")
async def shutdown():
    logger.debug("shutdown")


@app.middleware("http")
async def process_time(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    end = time.perf_counter()
    logger.debug(end - start)
    return response


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, debug=True)
