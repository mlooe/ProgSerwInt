"""Module containing user comic list service implementation."""

from typing import Iterable, Optional

from wirtualnykomiksapi.core.repositories.iuser_comic_list import IUserComicListRepository
from wirtualnykomiksapi.core.domain.user_comic_list import UserComicList, UserComicListBroker, UserComicListStatus
from wirtualnykomiksapi.infrastructure.dto.user_comic_listdto import UserComicListDTO
from wirtualnykomiksapi.infrastructure.services.iuser_comic_list import IUserComicListService

class UserComicListService(IUserComicListService):
    """A class implementing the user comic list service"""

    _repository: IUserComicListRepository

    def __init__(self, repository: IUserComicListRepository) -> None:
        """The initializer of the 'user comic list service'.

        Args:
            repository (IUserComicListRepository): The reference to the repository
        """

        self._repository = repository

    async def get_user_list(self, user_id: str) -> Iterable[UserComicListDTO]:
        """The method getting user's comic list

        Args:
            user_id (str): The id of the user

        Returns:
            Iterable[UserComicListDTO]: The collection of comics in users list
        """
        return await self._repository.get_user_list(user_id)

    async def add_comic(self, data: UserComicListBroker) -> UserComicListDTO:
        """The method adding comic to user's list

        Args:
            data (UserComicListBroker): The comic list data

        Returns:
            UserComicList: The comic list
        """
        return await self._repository.add_comic(str(data.user_id), data.comic_id)

    async def update_status(self, user_id: str, comic_id: int, status: str) -> Optional[UserComicListDTO]:
        """The method updating comic status in the user's list

        Args:
            user_id (str): The id of the user
            comic_id (int): The ID of the comic
            status (str): Status of the comic

        Returns:
            Optional[UserComicListDTO]: The updated status of the comic
        """

        if status not in [UserComicListStatus.PLANNING, UserComicListStatus.DROPPED, UserComicListStatus.READING, UserComicListStatus.COMPLETED]:
            raise ValueError("Unexpected status")

        return await self._repository.update_status(
            user_id=user_id,
            comic_id=comic_id,
            status=status,
        )

    async def delete_comic(self, user_id: str, comic_id: int) -> bool:
        """The method deleting comic from user's list

        Args:
            user_id (str): The id of the user
            comic_id (int): The id of the comic

        Returns:
            bool: Success of the operation
        """
        return await self._repository.delete_comic(user_id, comic_id)