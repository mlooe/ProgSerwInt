"""Model containing tag repository abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable, Any

from wirtualnykomiksapi.core.domain.tag import TagIn


class ITagRepository(ABC):
    """An abstract class representing protocol of tag repository"""

    @abstractmethod
    async def get_all_tags(self) -> Iterable[Any]:
        """Abstract method getting all tags from the repository

        Returns:
            Iterable[Any]: All the tags
        """

    @abstractmethod
    async def get_tag_by_id(self, tag_id: int) -> Any | None:
        """Abstract method getting tag by id

        Args:
            tag_id (int): The id of the tag

        Returns:
            Any | None: The tag
        """

    @abstractmethod
    async def add_tag(self, data: TagIn) -> Any | None:
        """Abstract method adding new tag

        Args:
            data (TagIn): An input tag

        Returns:
            Any | None: The tag
        """

    @abstractmethod
    async def update_tag(self, tag_id: int, data: TagIn) -> Any | None:
        """Abstract method updating existing tag

        Args:
            tag_id (int): The id of the tag we want to update
            data (TagIn): New tag data

        Returns:
            Any | None: The updated tag
        """

    @abstractmethod
    async def delete_tag(self, tag_id: int) -> bool:
        """Abstract method removing tag with given id

        Args:
            tag_id (int): The id of the tag

        Returns:
            bool: Success of the operation
        """