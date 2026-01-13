"""Module containing user comic list service abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable, Optional

from wirtualnykomiksapi.core.domain.user_comic_list import UserComicList, UserComicListBroker
from wirtualnykomiksapi.infrastructure.dto.user_comic_listdto import UserComicListDTO

class IUserComicListService(ABC):
    """A class representing user comic list repository"""

    @abstractmethod
    async def get_user_list(self, user_id: str) -> Iterable[UserComicListDTO]:
        """The method getting user's comic list

        Args:
            user_id (str): The id of the user

        Returns:
            Iterable[UserComicListDTO]: The collection of comics in users list
        """

    @abstractmethod
    async def add_comic(self, data: UserComicListBroker) -> UserComicListDTO:
        """The method adding comic to user's list

        Args:
            data (UserComicListBroker): The comic list data

        Returns:
            UserComicList: The comic list
        """

    @abstractmethod
    async def update_status(self, user_id: str, comic_id: int, status: str) -> Optional[UserComicListDTO]:
        """The method updating comic status in the user's list

        Args:
            user_id (str): The id of the user
            comic_id (int): The ID of the comic
            status (str): Status of the comic

        Returns:
            Optional[UserComicListDTO]: The updated status of the comic
        """

    @abstractmethod
    async def delete_comic(self, user_id: str, comic_id: int) -> bool:
        """The method deleting comic from user's list

        Args:
            user_id (str): The id of the user
            comic_id (int): The id of the comic

        Returns:
            bool: Success of the operation
        """
