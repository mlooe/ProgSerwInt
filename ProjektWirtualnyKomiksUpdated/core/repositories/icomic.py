"""Model containing comic repository abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable, Any

from core.domains.comic import Comic, ComicIn

class IComicRepository(ABC):
    """An abstract class representing protocol of comic repository"""

    @abstractmethod
    async def get_all_comics(self) -> Iterable[Any]:
        """Abstract method retrieving all comics from the data storage

        Returns:
            Iterable[Any]: The collection of the all countries.
        """

    @abstractmethod
    async def get_comic_by_id(self, comic_id: int) -> Any | None:
        """Abstract method getting comic by given id from the data storage

        Args:
            comic_id (int): The id of the comic.

        Returns:
            Any | None: The comic data if exists.
        """

    @abstractmethod
    async def get_comic_by_genres(self, genres: Iterable[str]) -> Iterable[Any]:
        """Abstract method getting comic by given genres from the data storage

        Args:
            genres (Iterable[str]): Genres collection

        Returns:
            Iterable[Any]: Filtered comics by provided collection of genres
        """

    @abstractmethod
    async def get_comic_by_tags(self, tags: Iterable[str]) -> Iterable[Any]:
        """Abstract method getting comic by given tags from the data storage

        Args:
            tags (Iterable[str]): Tags collection

        Returns:
            Iterable[Any]: Filtered comics by provided collection of tags
        """

    @abstractmethod
    async def add_comic(self, comic: ComicIn) -> Any:
        """Abstract method adding new comic to the data storage

        Args:
            comic (ComicIn): An input comic

        Returns:
            Any: The comic report
        """

    @abstractmethod
    async def update_comic(self, comic_id: int, data: ComicIn) -> Comic | None:
        """Abstract method updating existing comic in the data storage

        Args:
            comic_id (int): The ID of the comic we want to update
            data (ComicIn): New data of the comic

        Returns:
            Comic | None: The updated comic
        """

    @abstractmethod
    async def delete_comic(self, comic_id: int) -> bool:
        """Abstract method deleting comic with given id from the data storage

        Args:
            comic_id (int): The ID of the comic

        Returns:
            bool: Success of the operation
        """