"""Module containing comic service abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable

from core.domains.comic import Comic, ComicIn
from infrastructure.dto.comicdto import ComicDTO

class IComicService(ABC):
    """A class representing comic repository"""

    @abstractmethod
    async def get_all_comics(self) -> Iterable[ComicDTO]:
        """The method getting all comics from the repository

        Returns:
            Iterable[Comic]: All comics
        """

    @abstractmethod
    async def get_comic_by_id(self, comic_id: int) -> ComicDTO | None:
        """The method getting comics assigned to particular ID.

                Args:
                    comic_id (int): The id of the country.

                Returns:
                    Comic | None: The comic data if exists.
                """

    @abstractmethod
    async def get_comic_by_genres(self, genres: Iterable[str]) -> Iterable[Comic]:
        """The method getting comic by given genres from the data storage

        Args:
            genres (Iterable[str]): Genres collection

        Returns:
            Iterable[Any]: Filtered comics by provided collection of genres
        """

    @abstractmethod
    async def get_comic_by_tags(self, tags: Iterable[str]) -> Iterable[Comic]:
        """The method getting comic by given tags from the data storage

        Args:
            tags (Iterable[str]): Tags collection

        Returns:
            Iterable[Any]: Filtered comics by provided collection of tags
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