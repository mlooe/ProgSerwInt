from abc import ABC
from typing import Iterable
from zad2.domains.post_adress import PostRecord, CommentRecord

class IPostAdressRepository(ABC):
    async def get_posts(self) -> Iterable[PostRecord] | None:
        pass

    async def filter_posts(self, filtr: str) -> Iterable[PostRecord] | None:
        pass

    async def get_comments(self) -> Iterable[CommentRecord] | None:
        pass

    async def filter_comments(self, filtr: str) -> Iterable[CommentRecord] | None:
        pass
