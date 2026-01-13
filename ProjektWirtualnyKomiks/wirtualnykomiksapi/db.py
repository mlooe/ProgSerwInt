"""A module providing database access"""

import asyncio

import databases
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)

from wirtualnykomiksapi.config import config

metadata = sqlalchemy.MetaData()

# User table (UUID primary key)
user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    ),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
)

# Comics table
comic_table = sqlalchemy.Table(
    "comics",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("author", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("description", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("likes", sqlalchemy.Integer, nullable=False, default=0),
    sqlalchemy.Column("views", sqlalchemy.Integer, nullable=False, default=0),
    sqlalchemy.Column("user_id", UUID(as_uuid=True), sqlalchemy.ForeignKey("users.id"), nullable=False),
)

# Reviews table
review_table = sqlalchemy.Table(
    "reviews",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("comic_id", sqlalchemy.Integer ,sqlalchemy.ForeignKey("comics.id"), nullable=False),
    sqlalchemy.Column("user_id", UUID(as_uuid=True), sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("rating", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("comment", sqlalchemy.Text, nullable=True)

)

# Genre & Tag tables
genre_table = sqlalchemy.Table(
    "genres",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False, unique=True)
)

tag_table = sqlalchemy.Table(
    "tags",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False, unique=True)
)

# Association tables
comic_genre_table = sqlalchemy.Table(
    "comic_genres",
    metadata,
    sqlalchemy.Column("comic_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("comics.id"), primary_key=True),
    sqlalchemy.Column("genre_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("genres.id"), primary_key=True)
)

comic_tag_table = sqlalchemy.Table(
    "comic_tags",
    metadata,
    sqlalchemy.Column("comic_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("comics.id"), primary_key=True),
    sqlalchemy.Column("tag_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("tags.id"), primary_key=True)
)

# Users personal comic list
user_comic_list_table = sqlalchemy.Table(
    "user_comic_list",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", UUID(as_uuid=True), sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("comic_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("comics.id"), nullable=False),
    sqlalchemy.Column("status", sqlalchemy.String, nullable=False),
)


db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
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
