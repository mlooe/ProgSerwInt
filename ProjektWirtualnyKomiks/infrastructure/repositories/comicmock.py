"""Module containing comic repository implementation"""

from typing import Iterable

from core.repositories.icomic import IComicRepository
from core.domains.comic import Comic, ComicIn
from infrastructure.repositories.db import comics


class ComicMockRepository(IComicRepository):
    """A class representing comic repository."""

    async def get_all_comics(self) -> Iterable[Comic]:
        return comics

    async def get_comic_by_id(self, comic_id: int) -> Comic | None:
        return next((obj for obj in comics if obj.id == comic_id), None)

    async def add_comic(self, comic: ComicIn) -> None:
        comics.append(comic)

    async def update_comic(self, comic_id: int, data: ComicIn) -> Comic | None:
        if comic_pos := \
            next(filter(lambda x: x.id == comic_id, comics)):
            comics[comic_pos] = data
            return Comic(id=0, **data.model_dump())
        return None

    async def delete_comic(self, comic_id: int) -> bool:
        if comic_pos := \
            next(filter(lambda x: x.id == comic_id, comics)):
            comics.remove(comic_pos)
            return True
        return False

