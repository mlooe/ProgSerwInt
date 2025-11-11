"""Model containing user repository abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable

from core.domains.user import User, UserIn

class IUserRepository(ABC):
    """An abstract class representing protocol of user repository"""

    @abstractmethod
    async def get_all_users(self) -> Iterable[User]:
        """Abstract method retrieving all users from the data storage"""

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        """Abstract method getting user by given id from the data storage"""

    @abstractmethod
    async def add_user(self, user: UserIn) -> None:
        """Abstract method adding new user to the data storage"""

    @abstractmethod
    async def delete_user(self, user_id: int) -> None:
        """Abstract method deleting user with given id from the data storage"""