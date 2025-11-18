"""A module providing database access"""

import asyncio
import datetime

import databases
import sqlalchemy

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.mutable import MutableList
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)


from config import config

metadata = sqlalchemy.MetaData()

users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(50), nullable=False, unique=True),
    sqlalchemy.Column("email", sqlalchemy.String(120), nullable=False, unique=True),
    sqlalchemy.Column("password_hash", sqlalchemy.String(255), nullable=False),
)

db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

comics_table = sqlalchemy.Table(
    "comics",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("author_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
)

chapters_table = sqlalchemy.Table(
    "chapters",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("comic_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("comics.id")),
    sqlalchemy.Column("title", sqlalchemy.String(200)),
    sqlalchemy.Column("number", sqlalchemy.Integer, nullable=False),
)

pages_table = sqlalchemy.Table(
    "pages",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("chapter_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("chapters.id")),
    sqlalchemy.Column("page_number", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("image_url", sqlalchemy.String(300), nullable=False),
)

tags_table = sqlalchemy.Table(
    "tags",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50), unique=True, nullable=False),
)

comic_tags_table = sqlalchemy.Table(
    "comic_tags",
    metadata,
    sqlalchemy.Column("comic_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("comics.id")),
    sqlalchemy.Column("tag_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("tags.id")),
)

comments_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("comic_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("comics.id")),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("text", sqlalchemy.Text, nullable=False),
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
    force_rollback=True,
)

async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")
