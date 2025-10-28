from typing import List
from zad1.domains.post_adress import PostAdressRecord
from zad1.repositories.ipost_adress_repository import IPostAdressRepository


class PostAdressRepository(IPostAdressRepository):
    def __init__(self):
        self.storage: List[PostAdressRecord] = []

    async def save_posts(self, posts: List[PostAdressRecord]) -> None:
        self.storage = posts

    async def get_filtered(self, filtr: str) -> List[PostAdressRecord]:
        i = filtr.lower()
        return [post for post in self.storage if i in post.title.lower() or i in post.body.lower()]
