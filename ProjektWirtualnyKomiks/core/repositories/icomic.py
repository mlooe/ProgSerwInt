"""Model containing comic repository abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable

from core.domains.comic import Comic, ComicIn

class IComicRepository(ABC):
    """An abstract class representing protocol of comic repository"""

    @abstractmethod
    async def get_all_comics(self) -> Iterable[Comic]:
        """Abstract method retrieving all comics from the data storage"""

    @abstractmethod
    async def get_comic_by_id(self, comic_id: int) -> Comic | None:
        """Abstract method getting comic by given id from the data storage"""

    @abstractmethod
    async def get_comic_by_genres(self, genres: Iterable[str]) -> Iterable[Comic]:
        """Abstract method getting comic by given genres from the data storage"""

    @abstractmethod
    async def get_comic_by_tags(self, tags: Iterable[str]) -> Iterable[Comic]:
        """Abstract method getting comic by given tags from the data storage"""

    @abstractmethod
    async def add_comic(self, comic: ComicIn) -> None:
        """Abstract method adding new comic to the data storage"""

    @abstractmethod
    async def update_comic(self, comic_id: int, data: ComicIn) -> Comic | None:
        """Abstract method updating existing comic in the data storage"""

    @abstractmethod
    async def delete_comic(self, comic_id: int) -> bool:
        """Abstract method deleting comic with given id from the data storage"""