"""A repository for user entity"""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import UUID4

from wirtualnykomiksapi.core.domain.user import UserIn

class IUserRepository(ABC):
    """An abstract repository class for user repository"""

    @abstractmethod
    async def register_user(self, user: UserIn) -> Any | None:
        """The method registering new user

        Args:
            user (UserIn): The user input data

        Returns:
            Any | None: The new user object
        """

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID4) -> Any | None:
        """The method getting user by UUID

        Args:
            uuid (UUID5): UUID of the user

        Returns:
            Any | None: The user object if exists
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> Any | None:
        """The method getting user by email

        Args:
            email (str): The email of the user

        Returns:
            Any | None: The user object if exists
        """