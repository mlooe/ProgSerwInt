"""Module containing comic service abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable, Optional

from wirtualnykomiksapi.core.domain.comic import Comic, ComicIn, ComicBroker
from wirtualnykomiksapi.infrastructure.dto.comicdto import ComicDTO
from wirtualnykomiksapi.infrastructure.dto.comic_comparison_dto import ComicComparisonDTO

class IComicService(ABC):
    """A class representing comic repository"""

    @abstractmethod
    async def get_all_comics(self) -> Iterable[ComicDTO]:
        """The method getting all comics from the repository

        Returns:
            Iterable[ComicDTO]: All comics
        """

    @abstractmethod
    async def get_comic_by_id(self, comic_id: int) -> ComicDTO | None:
        """The method getting comics assigned to particular ID.

            Args:
                comic_id (int): The id of the comic

            Returns:
                ComicDTO | None: The comic data if exists
        """

    @abstractmethod
    async def get_filtered_comics(self, genres: Optional[str], tags: Optional[str]) -> Iterable[ComicDTO]:
        """The method getting filtered collection of comics

        Args:
            genres (Optional[str]): The list of genres
            tags (Optional[str]): The list of tags

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
    async def compare_comics(self, comic_id1: int, comic_id2: int) -> ComicComparisonDTO | None:
        """The method comparing two comics

        Args:
            comic_id1 (int): The id of the first comic
            comic_id2 (int): The id of the second comic

        Returns:
            ComicComparisonDTO | None: The comparison result
        """

    @abstractmethod
    async def get_most_popular_comics(self, limit: int) -> Iterable[Comic]:
        """The method getting comics with the most views

        Args:
            limit (int): The amount of shown comics

        Returns:
            Iterable[Any]: The collection of most viewed comics
        """

    @abstractmethod
    async def add_comic(self, comic: ComicBroker) -> ComicDTO | None:
        """The method adding new comic to the data storage

        Args:
            comic (ComicBroker): An input comic

        Returns:
            Comic: The comic
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