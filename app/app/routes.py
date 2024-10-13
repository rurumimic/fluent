import logging
import json
from typing import Union

from fastapi import APIRouter

from .logger import LOGGER_NAME

router = APIRouter()

logger = logging.getLogger(LOGGER_NAME)


@router.get("/")
async def home():
    logger.info("Hello, World!")
    return {"greeting": "Hello, World!"}


@router.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    logger.info({"item_id": item_id, "q": q})
    return {"item_id": item_id, "q": q}
