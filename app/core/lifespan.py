from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import Base, engine, models


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    yield

    print("end Creating tables...")