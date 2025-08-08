import uvicorn
from fastapi import FastAPI

from app.api.endpoints import app_router
from app.core import app_config
from app.core.lifespan import lifespan

app: FastAPI = FastAPI(
    debug=True,
    title=app_config.project_name,
    lifespan=lifespan
)

app.include_router(app_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=app_config.project_port,
        host=app_config.project_host,
    )