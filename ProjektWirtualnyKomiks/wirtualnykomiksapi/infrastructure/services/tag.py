"""Module containing tag service implementation."""

from typing import Iterable

from wirtualnykomiksapi.core.repositories.itag import ITagRepository
from wirtualnykomiksapi.core.domain.tag import Tag, TagIn
from wirtualnykomiksapi.infrastructure.dto.tagdto import TagDTO
from wirtualnykomiksapi.infrastructure.services.itag import ITagService

class TagService(ITagService):
    """A class implementing the tag service"""

    _repository: ITagRepository

    def __init__(self, repository: ITagRepository) -> None:
        """The initializer of the 'tag service'.

        Args:
            repository (ITagRepository): The reference to the repository
        """

        self._repository = repository

    async def get_all_tags(self) -> Iterable[TagDTO]:
        """The method getting all tags from the repository

        Returns:
            Iterable[TagDTO]: All the tags
        """
        return await self._repository.get_all_tags()

    async def get_tag_by_id(self, tag_id: int) -> TagDTO | None:
        """The method getting tag by id from the repository

        Args:
            tag_id (int): The id of the tag

        Returns:
            TagDTO | None: The tag
        """
        return await self._repository.get_tag_by_id(tag_id)

    async def add_tag(self, data: TagIn) -> Tag | None:
        """The method adding new tag to the repository

        Args:
            data (TagIn): An input tag
        Returns:
            Tag | None: The tag
        """
        return await self._repository.add_tag(data)

    async def update_tag(self, tag_id: int, data: TagIn) -> Tag | None:
        """The method updating tag in the repository

        Args:
            tag_id (int): The id of the tag
            data (TagIn): New tag data

        Returns:
            Tag | None: The updated tag
        """
        return await self._repository.update_tag(tag_id=tag_id, data=data)

    async def delete_tag(self, tag_id: int) -> bool:
        """The method removing tag with given id from the repository

        Args:
            tag_id (int): The id of the tag

        Returns:
            bool: Success of the operation
        """
        return await self._repository.delete_tag(tag_id)