"""Module containing airport repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from src.core.repositories.icomic import IComicRepository
from src.core.domain.comic import Comic, ComicIn

from src.db import (
comic_table,
database
)

from src.infrastructure.dto.comicdto import ComicDTO

class ComicRepository(IComicRepository):
    """A class representing comic DB repository"""

    async def get_all_comics(self) -> Iterable[Any]:
        """The method getting all airports from the data storage.

            Returns:
                Iterable[Any]: Airports in the data storage.
        """

        

