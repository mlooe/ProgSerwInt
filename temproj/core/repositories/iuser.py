"""Model containing user repository abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable, Any

from core.domains.user import User, UserIn

class IUserRepository(ABC):
    """An abstract class representing protocol of user repository"""

    @abstractmethod
    async def get_all_users(self) -> Iterable[User]:
        """Abstract method retrieving all users from the data storage

        Returns:
            Iterable[User]: Users in the data storage
        """

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        """Abstract method getting user by given id from the data storage

        Args:
            user_id: ID of the user

        Returns:
            User | None: The user object if it exists
        """

    @abstractmethod
    async def add_user(self, user: UserIn) -> Any | None:
        """Abstract method adding new user to the data storage

        Args:
            user (userIn): The user input data

        Returns:
            Any | None: The newly created user
        """


    @abstractmethod
    async def delete_user(self, user_id: int) -> bool:
        """Abstract method deleting user with given id from the data storage

        Args:
            user_id (int): The user id

        Returns:
            bool: Success of the operation
        """
