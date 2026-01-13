"""Module containing comic service implementation."""

from typing import Iterable, Optional

from wirtualnykomiksapi.core.repositories.icomic import IComicRepository
from wirtualnykomiksapi.core.domain.comic import Comic, ComicIn, ComicBroker
from wirtualnykomiksapi.infrastructure.dto.comicdto import ComicDTO
from wirtualnykomiksapi.infrastructure.dto.comic_comparison_dto import ComicComparisonDTO
from wirtualnykomiksapi.infrastructure.services.icomic import IComicService

class ComicService(IComicService):
    """A class implementing the comic service"""

    _repository: IComicRepository

    def __init__(self, repository: IComicRepository) -> None:
        """The initializer of the 'comic service'.

        Args:
            repository (IComicRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all_comics(self) -> Iterable[ComicDTO]:
        """The method getting all comics from the repository.

        Returns:
            Iterable[ComicDTO]: All comics.
        """

        return await self._repository.get_all_comics()

    async def get_comic_by_id(self, comic_id: int) -> ComicDTO | None:
        """The method getting comic by provided id.

        Args:
            comic_id (int): The id of the comic.

        Returns:
            ComicDTO | None: The comic details.
        """

        return await self._repository.get_comic_by_id(comic_id)

    async def get_filtered_comics(self, genres: Optional[str], tags: Optional[str]) -> Iterable[ComicDTO]:
        """The method getting filtered collection of comics

        Args:
            genres (Optional[str]): The list of genres
            tags (Optional[str]): The list of tags

        Returns:
            Iterable[ComicDTO]: The filtered collection of comics
        """
        return await self._repository.get_filtered_comics(genres, tags)

    async def get_most_popular_comics(self, limit: int) -> Iterable[Comic]:
        """The method getting most popular comics

        Args:
             limit (int): The amount of comics

        Returns:
            Iterable[Comic]: The comics
        """
        return await self._repository.get_most_popular_comics(limit)

    async def compare_comics(self, comic_id1: int, comic_id2: int) -> ComicComparisonDTO | None:
        """The method comparing two comics

        Args:
            comic_id1 (int): The ID of the first comic
            comic_id2 (int): The ID of the second comic

        Returns:
            ComicComparisonDTO | None: The comparison result
        """
        return await self._repository.compare_comics(comic_id1, comic_id2)
        
        
    async def get_top_rated_comics(self, limit: int) -> Iterable[Comic]:
        """The method getting comics with the highest average rating

        Args:
            limit (int): The amount of shown comics

        Returns:
            Iterable[Any]: The collection of highest average rated comics
        """
        return await self._repository.get_top_rated_comics(limit)


    async def add_comic(self, data: ComicBroker) -> ComicDTO | None:
        """The method adding new comic to the repository

        Args:
            data (ComicBroker): An input comic

        Returns:
            Comic | None: Full details of the newly added comic
        """
        return await self._repository.add_comic(data)

    async def update_comic(self, comic_id: int, data: ComicIn) -> Comic | None:
        """The method updating existing comic in the repository

        Args:
            comic_id (int): The ID of the comic we want to update
            data (ComicIn): New data of the comic

        Returns:
            Comic | None: The updated comic
        """
        return await self._repository.update_comic(
            comic_id=comic_id,
            data=data,
        )

    async def delete_comic(self, comic_id: int) -> bool:
        """The method removing comic with given id from the repository

        Args:
            comic_id (int): The ID of the comic

        Returns:
            bool: Success of the operation
        """
        return await self._repository.delete_comic(comic_id)
