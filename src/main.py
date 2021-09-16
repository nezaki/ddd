import uvicorn

from fastapi import FastAPI

from src.presentation.controller.project import router as project_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass

app.include_router(project_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, debug=True)
