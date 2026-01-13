"""Module containing genre service implementation."""

from typing import Iterable, Optional

from wirtualnykomiksapi.core.repositories.igenre import IGenreRepository
from wirtualnykomiksapi.core.domain.genre import Genre, GenreIn
from wirtualnykomiksapi.infrastructure.dto.genredto import GenreDTO
from wirtualnykomiksapi.infrastructure.services.igenre import IGenreService

class GenreService(IGenreService):
    """A class implementing the genre service"""

    _repository: IGenreRepository

    def __init__(self, repository: IGenreRepository) -> None:
        """The initializer of the 'genre service'.

        Args:
            repository (IGenreRepository): The reference to the repository
        """

        self._repository = repository

    async def get_all_genres(self) -> Iterable[GenreDTO]:
        """The method getting all genres from the repository

        Returns:
            Iterable[GenreDTO]: All the genres
        """
        return await self._repository.get_all_genres()

    async def get_genre_by_id(self, genre_id: int) -> GenreDTO | None:
        """The method getting genre by id

        Args:
            genre_id (int): The id of the genre

        Returns:
            Optional[GenreDTO]: The genre
        """
        return await self._repository.get_genre_by_id(genre_id)

    async def add_genre(self, data: GenreIn) -> Genre | None:
        """The method adding new genre to the data storage

        Args:
            data (GenreIn): An input genre

        Returns:
            Genre | None: The genre
        """
        return await self._repository.add_genre(data)

    async def update_genre(self, genre_id: int, data: GenreIn) -> Genre | None:
        """The method updating genre in the data storage

        Args:
            genre_id (int): The ID of the genre we want to update
            data (GenreIn): New genre data

        Returns:
            Genre | None: The updated genre
        """
        return await self._repository.update_genre(genre_id=genre_id, data=data)

    async def delete_genre(self, genre_id: int) -> bool:
        """The method removing genre with given id from the data storage

        Args:
            genre_id (int): The id of the genre

        Returns:
            bool: Success of the operation
        """
        return await self._repository.delete_genre(genre_id)