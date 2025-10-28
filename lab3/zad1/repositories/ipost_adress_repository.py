from abc import ABC
from typing import List
from zad1.domains.post_adress import PostAdressRecord

class IPostAdressRepository(ABC):
    async def save_posts(self, posts: List[PostAdressRecord]) -> None:
        pass

    async def get_filtered(self, filtr: str) -> List[PostAdressRecord]:
        pass