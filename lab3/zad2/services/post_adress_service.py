import asyncio
from typing import Iterable
from zad2.repositories.post_adress_repository import PostAdressRepository
from zad2.services.ipost_adress_service import IPostAdressService

class PostAdressService(IPostAdressService):
    def __init__(self, repository: PostAdressRepository):
        self.repository = repository

    async def load_data(self):
        await asyncio.gather(
            self.repository.get_posts(),
            self.repository.get_comments()
        )

    async def filter(self, text: str) -> Iterable:
        return await self.repository.filter_posts(text)

    async def sort_by_usage(self) -> Iterable:
        return await self.repository.sort_by_last_used()

    async def cleanup(self, seconds: int):
        while True:
            await asyncio.sleep(seconds)
            await self.repository.cleanup_unused(seconds)