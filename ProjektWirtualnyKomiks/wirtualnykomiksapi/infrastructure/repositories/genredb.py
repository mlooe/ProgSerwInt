"""Module containing genre repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from wirtualnykomiksapi.core.domain.genre import Genre, GenreIn
from wirtualnykomiksapi.core.repositories.igenre import IGenreRepository

from wirtualnykomiksapi.db import (
    database,
    genre_table,
)

from wirtualnykomiksapi.infrastructure.dto.genredto import GenreDTO

class GenreRepository(IGenreRepository):
    """A class representing genre DB repository"""

    async def get_all_genres(self) -> Iterable[Any]:
        """The method getting all genres from the repository

        Returns:
            Iterable[Any]: All genres
        """
        query = (
            select(
                genre_table.c.id,
                genre_table.c.name,
            )
            .order_by(genre_table.c.id)
        )
        genres = await database.fetch_all(query)

        return [GenreDTO(**dict(genre)) for genre in genres]

    async def get_genre_by_id(self, genre_id: int) -> Any | None:
        """The method getting genre by id

        Args:
            genre_id (int): The id of the genre

        Returns:
            Any | None: The genre
        """

        genre = await self._get_by_id(genre_id)
        return Genre(**dict(genre)) if genre else None

    async def add_genre(self, data: GenreIn) -> Any | None:
        """The method adding new genre

        Args:
            data (GenreIn): An input genre

        Returns:
            Any | None: The genre
        """

        query = genre_table.insert().values(**data.model_dump())
        new_genre_id = await database.execute(query)
        new_genre = await self._get_by_id(new_genre_id)

        return Genre(**dict(new_genre)) if new_genre else None

    async def update_genre(self, genre_id: int, data: GenreIn) -> Any | None:
        """The method updating existing genre

        Args:
            genre_id (int): The id of the genre we want to update
            data (GenreIn): New genre data

        Returns:
            Any | None: The updated genre
        """

        if self._get_by_id(genre_id):
            query = (
                genre_table.update()
                .where(genre_table.c.id == genre_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            genre = await self._get_by_id(genre_id)
            return Genre(**dict(genre)) if genre else None

        return None

    async def delete_genre(self, genre_id: int) -> bool:
        """The method removing genre with given id

        Args:
            genre_id (int): The id of the genre

        Returns:
            bool: Success of the operation
        """

        if self._get_by_id(genre_id):
            query = genre_table \
                .delete() \
                .where(genre_table.c.id == genre_id)

            await database.execute(query)
            return True

        return False


    async def _get_by_id(self, genre_id: int) -> Record | None:
        """A private method getting genre from the database based on its id

        Args:
            genre_id (int): The id of the genre

        Returns:
            Record | None: Genre record if it exists
        """
        query = (
            genre_table.select()
            .where(genre_table.c.id == genre_id)
            .order_by(genre_table.c.id)
        )
        return await database.fetch_one(query)