"""Model containing genre repository abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable, Any

from wirtualnykomiksapi.core.domain.genre import GenreIn


class IGenreRepository(ABC):
    """An abstract class representing protocol of genre repository"""

    @abstractmethod
    async def get_all_genres(self) -> Iterable[Any]:
        """Abstract method getting all genres from the repository

        Returns:
            Iterably[Any]: All the genres
        """

    @abstractmethod
    async def get_genre_by_id(self, genre_id: int) -> Any | None:
        """Abstract method getting genre by id

        Args:
            genre_id (int): The id of the genre

        Returns:
            Any | None: The genre
        """

    @abstractmethod
    async def add_genre(self, data: GenreIn) -> Any | None:
        """Abstract method adding new genre

        Args:
            data (GenreIn): An input genre

        Returns:
            Any | None: The genre
        """

    @abstractmethod
    async def update_genre(self, genre_id: int, data: GenreIn) -> Any | None:
        """Abstract method updating existing genre

        Args:
            genre_id (int): The id of the genre we want to update
            data (GenreIn): New genre data

        Returns:
            Any | None: The updated genre
        """

    @abstractmethod
    async def delete_genre(self, genre_id: int) -> bool:
        """The method removing genre with given id

        Args:
            genre_id (int): The id of the genre

        Returns:
            bool: Success of the operation

        """