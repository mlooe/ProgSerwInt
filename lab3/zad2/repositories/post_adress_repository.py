import asyncio
import aiohttp

from time import time
from typing import Iterable
from zad2.domains.post_adress import PostRecord, CommentRecord
from zad2.repositories.ipost_adress_repository import IPostAdressRepository
from zad2.utils import consts

class PostAdressRepository(IPostAdressRepository):
    def __init__(self):
        self._post_adress_repository: Iterable[PostRecord] = []
        self._comment_repository: Iterable[CommentRecord] = []

    async def get_posts(self) -> Iterable[PostRecord] | None:
        posts = await self._get_posts()
        self._post_adress_repository = await self._parse_posts(posts)

        for post in self._post_adress_repository:
            post.last_used = time()

        return self._post_adress_repository


    async def filter_posts(self, text: str) -> Iterable[PostRecord] | None:
        text = text.lower()
        posts = await self.get_posts()
        comments = await self.get_comments()
        filtered = []

        for post in posts:
            match = False
            if text in post.title.lower() or text in post.body.lower():
                match = True

            if not match:
                for c in comments:
                    if c.postId == post.id and (text in c.name.lower() or text in c.body.lower()):
                        match = True
                        c.last_used = time()
                        break
            if match:
                post.last_used = time()
                filtered.append(post)
        return filtered



    async def sort_by_last_used(self) -> Iterable[PostRecord]:
        posts = await self.get_posts()
        posts_sorted = sorted(posts, key=lambda p: p.last_used, reverse=True)
        return posts_sorted


    async def get_comments(self) -> Iterable[CommentRecord] | None:
        comments = await self._get_comments()
        self._comment_repository = await self._parse_comments(comments)

        for comment in self._comment_repository:
            comment.last_used = time()

        return self._comment_repository


    async def cleanup_unused(self, seconds: int):
        now = time()
        self._post_adress_repository = [p for p in self._post_adress_repository if now - p.last_used <= seconds]
        self._comment_repository = [c for c in self._comment_repository if now - c.last_used <= seconds]


    async def _get_comments(self) -> Iterable[dict] | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(consts.API_COMMENTS_URL) as response:
                if response.status != 200:
                    return None

                return await response.json()


    async def _parse_comments(self, params: Iterable[dict]) -> Iterable[CommentRecord]:
        return [CommentRecord(postId=comment.get("postId"),
                              id=comment.get("id"),
                              name=comment.get("name"),
                              email=comment.get("email"),
                              body=comment.get("body")) for comment in params]

    async def _get_posts(self) -> Iterable[dict] | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(consts.API_POSTS_URL) as response:
                if response.status != 200:
                    return None
                return await response.json()


    async def _parse_posts(self, params: Iterable[dict]) -> Iterable[PostRecord]:
        return [PostRecord(userId=post.get("userId"),
                           id=post.get("id"),
                           title=post.get("title"),
                           body=post.get("body")) for post in params]


