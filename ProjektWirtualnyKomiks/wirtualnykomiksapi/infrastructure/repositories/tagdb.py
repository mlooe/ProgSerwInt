"""Module containing tag repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from wirtualnykomiksapi.core.domain.tag import Tag, TagIn
from wirtualnykomiksapi.core.repositories.itag import ITagRepository

from wirtualnykomiksapi.db import (
    database,
    tag_table,
)

from wirtualnykomiksapi.infrastructure.dto.tagdto import TagDTO

class TagRepository(ITagRepository):
    """A class representing tag DB repository"""

    async def get_all_tags(self) -> Iterable[Any]:
        """The method getting all tags from the repository

        Returns:
            Iterable[Any]: All tags
        """
        query = (
            select(
                tag_table.c.id,
                tag_table.c.name,
            )
            .order_by(tag_table.c.id)
        )
        tags = await database.fetch_all(query)

        return [TagDTO(**dict(tag)) for tag in tags]

    async def get_tag_by_id(self, tag_id: int) -> Any | None:
        """The method getting tag by id

        Args:
            tag_id (int): The id of the tag

        Returns:
            Any | None: The tag
        """

        tag = await self._get_by_id(tag_id)
        return Tag(**dict(tag)) if tag else None

    async def add_tag(self, data: TagIn) -> Any | None:
        """The method adding new tag

        Args:
            data (TagIn): An input tag

        Returns:
            Any | None: The tag
        """

        query = tag_table.insert().values(**data.model_dump())
        new_tag_id = await database.execute(query)
        new_tag = await self._get_by_id(new_tag_id)

        return Tag(**dict(new_tag)) if new_tag else None

    async def update_tag(self, tag_id: int, data: TagIn) -> Any | None:
        """The method updating existing tag

        Args:
            tag_id (int): The id of the tag we want to update
            data (TagIn): New tag data

        Returns:
            Any | None: The updated tag
        """

        if self._get_by_id(tag_id):
            query = (
                tag_table.update()
                .where(tag_table.c.id == tag_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            tag = await self._get_by_id(tag_id)
            return Tag(**dict(tag)) if tag else None

        return None

    async def delete_tag(self, tag_id: int) -> bool:
        """The method removing tag with given id

        Args:
            tag_id (int): The id of the tag

        Returns:
            bool: Success of the operation
        """

        if self._get_by_id(tag_id):
            query = tag_table \
                .delete() \
                .where(tag_table.c.id == tag_id)

            await database.execute(query)
            return True

        return False

    async def _get_by_id(self, tag_id: int) -> Record | None:
        """A private method getting tag from the database based on its id

        Args:
            tag_id (int): The id of the tag

        Returns:
            Record | None: Tag record if it exists
        """
        query = (
            tag_table.select()
            .where(tag_table.c.id == tag_id)
            .order_by(tag_table.c.id)
        )
        return await database.fetch_one(query)