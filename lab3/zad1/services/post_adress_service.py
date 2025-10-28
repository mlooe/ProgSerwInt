import aiohttp

from zad1.repositories.post_adress_repository import IPostAdressRepository
from zad1.services.ipost_adress_service import IPostAdressService
from typing import List
from zad1.domains.post_adress import PostAdressRecord

class PostAdressService(IPostAdressService):
    repository: IPostAdressRepository

    def __init__(self, repository: IPostAdressRepository) -> None:
        self.repository = repository

    async def load_posts(self, url: str) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        posts = []
        for p in data:
            posts.append(PostAdressRecord(**p))
        await self.repository.save_posts(posts)

    async def search(self, text: str) -> List[PostAdressRecord]:
        return await self.repository.get_filtered(text)