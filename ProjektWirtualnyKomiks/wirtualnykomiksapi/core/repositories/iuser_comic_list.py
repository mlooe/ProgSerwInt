"""Model containing user comic list repository abstractions"""

from abc import ABC, abstractmethod
from typing import Any, Iterable, List, Optional

from pydantic import UUID4

from wirtualnykomiksapi.core.domain.user_comic_list import UserComicListIn


class IUserComicListRepository(ABC):
    """An abstract class representing protocol of user's comic list repository"""

    @abstractmethod
    async def get_user_list(self, user_id: str) -> Iterable[Any]:
        """Abstract method getting user's comic list

        Args:
            user_id (str): The id of the user

        Returns:
            Iterable[Any]: The collection of comics in users list
        """

    @abstractmethod
    async def add_comic(self, user_id: str, comic_id: int) -> Any:
        """Abstract method adding comic to user's list

        Args:
            user_id (str): The id of the user
            comic_id (int): The ID of the comic

        Returns:
            Any: The comic
        """

    @abstractmethod
    async def update_status(self, user_id: str, comic_id: int, status: str) -> Optional[Any]:
        """Abstract method updating comic status in the user's list

        Args:
            user_id (str): The id of the user
            comic_id (int): The ID of the comic
            status (str): Status of the comic

        Returns:
            Optional[Any]: The updated status of the comic
        """

    @abstractmethod
    async def delete_comic(self, user_id: str, comic_id: int) -> bool:
        """Abstract method deleting comic from user's list

        Args:
            user_id (str): The id of the user
            comic_id (int): The ID of the comic

        Returns:
            bool: Success of the operation
        """