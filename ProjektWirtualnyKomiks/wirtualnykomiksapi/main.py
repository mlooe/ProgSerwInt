"""Main module of the app"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from wirtualnykomiksapi.api.routers.comic import router as comic_router
from wirtualnykomiksapi.api.routers.review import router as review_router
from wirtualnykomiksapi.api.routers.genre import router as genre_router
from wirtualnykomiksapi.api.routers.tag import router as tag_router
from wirtualnykomiksapi.api.routers.user_comic_list import router as user_comic_list_router
from wirtualnykomiksapi.api.routers.user import router as user_router
from wirtualnykomiksapi.container import Container
from wirtualnykomiksapi.db import database, init_db

container = Container()
container.wire(modules=[
    "wirtualnykomiksapi.api.routers.comic",
    "wirtualnykomiksapi.api.routers.review",
    "wirtualnykomiksapi.api.routers.genre",
    "wirtualnykomiksapi.api.routers.tag",
    "wirtualnykomiksapi.api.routers.user",
    "wirtualnykomiksapi.api.routers.user_comic_list",
])

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(comic_router, prefix="/comic")
app.include_router(review_router, prefix="/review")
app.include_router(genre_router, prefix="/genre")
app.include_router(tag_router, prefix="/tag")
app.include_router(user_router, prefix="")
app.include_router(user_comic_list_router, prefix="/user_comic_list")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)
