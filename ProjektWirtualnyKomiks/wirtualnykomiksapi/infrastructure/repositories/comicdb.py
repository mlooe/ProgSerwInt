"""Module containing comic repository implementation"""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from wirtualnykomiksapi.core.repositories.icomic import IComicRepository
from wirtualnykomiksapi.core.domain.comic import Comic, ComicIn
from wirtualnykomiksapi.db import (
    comic_table,
    database,
)


class ComicRepository(IComicRepository):
    """A class implementing the comic repository"""

    async def get_comic_by_id(self, comic_id: int) -> Any | None:
        """The method getting a comic from the temporary data storage.

        Args:
            comic_id (int): The id of the comic.

        Returns:
            Any | None: The country data if exists.
        """

        comic = await self._get_by_id(comic_id)

        return Comic(**dict(comic)) if comic else None

    async def get_all_comics(self) -> Iterable[Any]:
        """The method getting all comics from the data storage

        Returns:
            Iterable[Any]: The collection of all the comics
        """

        query = comic_table.select().order_by(comic_table.c.name.asc())
        countries = await database.fetch_all(query)

        return [Comic(**dict(country)) for country in countries]

    async def add_comic(self, data: ComicIn) -> Any | None:
        """The method adding new comic to the data storage

        Args:
            data (ComicIn): An input comic

        Returns:
            Any | None: The comic report
        """

        query = comic_table.insert().values(**data.model_dump())
        new_comic_id = await database.execute(query)
        new_comic = await self._get_by_id(new_comic_id)

        return Comic(**dict(new_comic)) if new_comic else None

    async def _get_by_id(self, country_id: int) -> Record | None:
        """A private method getting country from the DB based on its ID.

        Args:
            country_id (int): The ID of the country.

        Returns:
            Any | None: Country record if exists.
        """

        query = (
            comic_table.select()
            .where(comic_table.c.id == country_id)
            .order_by(comic_table.c.name.asc())
        )

        return await database.fetch_one(query)