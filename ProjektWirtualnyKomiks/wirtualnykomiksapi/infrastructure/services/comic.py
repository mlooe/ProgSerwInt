"""Module containing continent service implementation."""

from typing import Iterable, Optional, List

from core.repositories.icomic import IComicRepository
from core.domain.comic import Comic, ComicIn
from infrastructure.dto.comicdto import ComicDTO
from infrastructure.services.icomic import IComicService

class ComicService(IComicService):
    """A class implementing the comic service"""

    _repository: IComicRepository

    def __init__(self, repository: IComicRepository) -> None:
        """The initializer of the `airport service`.

        Args:
            repository (IAirportRepository): The reference to the repository.
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
            ComicDTO | None: The airport details.
        """

        return await self._repository.get_comic_by_id(comic_id)

    async def get_filtered_comics(self, genres: Optional[List[int]], tags: Optional[List[int]]) -> Iterable[ComicDTO]:
        """The method getting filtered by provided genres and tags

        Args:
            genres (Optional[List[int]]): The list of genre ids
            tags (Optional[List[int]]): The list of tag ids

        Returns:
            Iterable[ComicDTO]: The filtered collection of comics
        """

        return await self._repository.get_filtered_comics(genres, tags)

    async def add_comic(self, data: ComicIn) -> Comic | None:
        """The method adding new comic to the data storage

        Args:
            data (ComicIn): An input comic

        Returns:
            Comic | None: Full details of the newly added comic
        """

        return await self._repository.add_comic(data)

    async def update_comic(self, comic_id: int, data: ComicIn) -> Comic | None:
        """The method updating existing comic in the data storage

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
        """The method removing comic with given id from the data storage

        Args:
            comic_id (int): The ID of the comic

        Returns:
            bool: Success of the operation
        """

        return await self._repository.delete_comic(comic_id)

    # do dokończenia
