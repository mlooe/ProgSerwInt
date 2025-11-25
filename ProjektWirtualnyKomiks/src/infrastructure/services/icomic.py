"""Module containing comic service abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable, Optional, List, Any

from src.core.domain.comic import Comic, ComicIn

class IComicService(ABC):
    """A class representing comic repository"""

    @abstractmethod
    async def get_all_comics(self) -> Iterable[Comic]:
        """The method getting all comics from the repository

        Returns:
            Iterable[ComicDTO]: All comics
        """

    @abstractmethod
    async def get_comic_by_id(self, comic_id: int) -> Comic | None:
        """The method getting comics assigned to particular ID.

            Args:
                comic_id (int): The id of the country.

            Returns:
                ComicDTO | None: The comic data if exists.
        """

    @abstractmethod
    async def get_filtered_comics(self, genres: Optional[List[int]], tags: Optional[List[int]]) -> Iterable[Comic]:
        """The method getting filtered collection of comics

        Args:
            genres (Optional[List[int]]): The list of genres
            tags (Optional[List[int]]): The list of tags

        Returns:
            Iterable[ComicDTO]: The filtered collection of comics
        """

    @abstractmethod
    async def get_top_rated_comics(self, limit: int) -> Iterable[Comic]:
        """The method getting comics with the highest average rating

        Args:
            limit (int): The amount of shown comics

        Returns:
            Iterable[Any]: The collection of highest average rated comics
        """

    @abstractmethod
    async def get_most_popular_comics(self, limit: int) -> Iterable[Comic]:
        """The method getting comics with the most likes or views

        Args:
            limit (int): The amount of shown comics

        Returns:
            Iterable[Any]: The collection of most liked/viewed comics
        """


    @abstractmethod
    async def add_comic(self, comic: ComicIn) -> Comic:
        """The method adding new comic to the data storage

        Args:
            comic (ComicIn): An input comic

        Returns:
            Any: The comic report
        """

    @abstractmethod
    async def update_comic(self, comic_id: int, data: ComicIn) -> Comic | None:
        """The method updating existing comic in the data storage

        Args:
            comic_id (int): The ID of the comic we want to update
            data (ComicIn): New data of the comic

        Returns:
            Comic | None: The updated comic
        """

    @abstractmethod
    async def delete_comic(self, comic_id: int) -> bool:
        """The method removing comic with given id from the data storage

        Args:
            comic_id (int): The ID of the comic

        Returns:
            bool: Success of the operation
        """