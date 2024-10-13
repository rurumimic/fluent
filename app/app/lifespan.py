from contextlib import asynccontextmanager

from fastapi import FastAPI

from .logger import FluentLogger


@asynccontextmanager
async def lifespan(app: FastAPI):
    fluent_logger = FluentLogger(propagate=False)
    yield
    fluent_logger.close()
