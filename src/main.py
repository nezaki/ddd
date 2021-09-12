from fastapi import FastAPI
from src.presentation.controller.project import router as project_router
from starlette.requests import Request

app = FastAPI()


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass

app.include_router(project_router)
