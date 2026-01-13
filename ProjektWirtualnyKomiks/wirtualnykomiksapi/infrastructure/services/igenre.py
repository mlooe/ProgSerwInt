"""Module containing genre service abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable, Optional, List, Any

from wirtualnykomiksapi.core.domain.genre import Genre, GenreIn
from wirtualnykomiksapi.infrastructure.dto.genredto import GenreDTO

class IGenreService(ABC):
    """A class representing genre repository"""

    @abstractmethod
    async def get_all_genres(self) -> Iterable[GenreDTO]:
        """The method getting all genres from the repository

        Returns:
            Iterable[GenreDTO]: All genres
        """

    @abstractmethod
    async def get_genre_by_id(self, genre_id: int) -> GenreDTO | None:
        """The method getting genre by id

        Args:
            genre_id (int): The id of the genre

        Returns:
            Optional[GenreDTO]: The genre
        """

    @abstractmethod
    async def add_genre(self, data: GenreIn) -> Genre | None:
        """The method adding new genre to the data storage

        Args:
            data (GenreIn): An input genre

        Returns:
            Genre | None: The genre
        """

    @abstractmethod
    async def update_genre(self, genre_id: int, data: GenreIn) -> Genre | None:
        """The method updating genre in the data storage

        Args:
            genre_id (int): The ID of the genre we want to update
            data (GenreIn): New genre data

        Returns:
            Genre | None: The updated genre
        """

    @abstractmethod
    async def delete_genre(self, genre_id: int) -> bool:
        """The method removing genre with given id from the data storage

        Args:
            genre_id (int): The id of the genre

        Returns:
            bool: Success of the operation
        """
