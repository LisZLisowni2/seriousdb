from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI

from .cache import Cache
from .config import validate_config

cache = Cache()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_file_path = validate_config()
    cache.load(db_file_path)
    yield


app = FastAPI(lifespan=lifespan)


def get_cache() -> Cache:
    return cache


@app.put("/db")
def put(
    key: str,
    value: str,
    background_tasks: BackgroundTasks,
    cache: Annotated[Cache, Depends(get_cache)],
):
    cache.insert(key, value)
    background_tasks.add_task(cache.flush)
    return value


@app.get("/db")
def get(key: str, cache: Annotated[Cache, Depends(get_cache)]):
    return cache.select(key)


@app.delete("/db")
def delete(key: str, cache: Annotated[Cache, Depends(get_cache)]):
    return cache.delete(key)
