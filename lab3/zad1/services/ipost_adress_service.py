from abc import ABC
from typing import List
from zad1.domains.post_adress import PostAdressRecord

class IPostAdressService(ABC):
    async def load_posts(self, url: str) -> None:
        pass

    async def search(self, text: str) -> List[PostAdressRecord]:
        pass
