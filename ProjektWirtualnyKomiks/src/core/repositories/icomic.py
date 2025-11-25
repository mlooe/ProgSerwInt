"""Model containing comic repository abstractions"""

from abc import ABC, abstractmethod
from typing import Any, Iterable, List, Optional

from src.core.domain.comic import Comic, ComicIn

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
    async def get_filtered_comics(self, genres: Optional[List[int]], tags: Optional[List[int]]) -> Iterable[Any]:
        """Abstract method getting filtered collection of comics

        Args:
            genres (Optional[List[int]]): The list of genres
            tags (Optional[List[int]]): The list of tags

        Returns:
            Iterable[Any]: The filtered collection of comics
        """

    @abstractmethod
    async def get_top_rated_comics(self, limit: int) -> Iterable[Any]:
        """Abstract method getting comics with the highest average rating

        Args:
            limit (int): The amount of shown comics

        Returns:
            Iterable[Any]: The collection of highest average rated comics
        """

    @abstractmethod
    async def get_most_popular_comics(self, limit: int) -> Iterable[Any]:
        """Abstract method getting comics with the most likes or views

        Args:
            limit (int): The amount of shown comics

        Returns:
            Iterable[Any]: The collection of most liked/viewed comics
        """

    @abstractmethod
    async def add_comic(self, data: ComicIn) -> Any | None:
        """Abstract method adding new comic to the data storage

        Args:
            data (ComicIn): An input comic

        Returns:
            Any | None: The comic report
        """

    @abstractmethod
    async def update_comic(self, comic_id: int, data: ComicIn) -> Any | None:
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