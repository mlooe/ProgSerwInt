"""Module containing tag service abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable

from wirtualnykomiksapi.core.domain.tag import Tag, TagIn
from wirtualnykomiksapi.infrastructure.dto.tagdto import TagDTO

class ITagService(ABC):
    """A class representing tag repository"""

    @abstractmethod
    async def get_all_tags(self) -> Iterable[TagDTO]:
        """The method getting all tags from the repository

        Returns:
            Iterable[TagDTO]: All the tags
        """

    @abstractmethod
    async def get_tag_by_id(self, tag_id: int) -> TagDTO | None:
        """The method getting tag by id

        Args:
            tag_id (int): The id of the tag

        Returns:
            TagDTO | None: The tag
        """

    @abstractmethod
    async def add_tag(self, data: TagIn) -> Tag | None:
        """The method adding new tag

        Args:
            data (TagIn): An input tag

        Returns:
            Tag | None: The tag
        """

    @abstractmethod
    async def update_tag(self, tag_id: int, data: TagIn) -> Tag | None:
        """The method updating existing tag

        Args:
            tag_id (int): The id of the tag we want to update
            data (TagIn): New tag data

        Returns:
            Tag | None: The updated tag
        """

    @abstractmethod
    async def delete_tag(self, tag_id: int) -> bool:
        """The method removing tag with given id

        Args:
            tag_id (int): The id of the tag

        Returns:
            bool: Success of the operation
        """