"""A repository for user entity"""

from typing import Any
from pydantic import UUID4

from wirtualnykomiksapi.infrastructure.utils.password import hash_password
from wirtualnykomiksapi.core.repositories.iuser import IUserRepository
from wirtualnykomiksapi.core.domain.user import UserIn
from wirtualnykomiksapi.db import (
    database,
    user_table
)

class UserRepository(IUserRepository):
    """An implementation of repository class for user"""

    async def register_user(self, user: UserIn) -> Any | None:
        """The method registering new user

        Args:
            user (UserIn): The user input data

        Returns:
            Any | None: The new user object
        """

        if await self.get_by_email(user.email):
            return None

        user.password = hash_password(user.password)

        query = user_table.insert().values(**user.model_dump())
        new_user_uuid = await database.execute(query)

        return await self.get_by_uuid(new_user_uuid)

    async def get_by_uuid(self, uuid: UUID4) -> Any | None:
        """The method getting user by UUID

        Args:
            uuid (UUID4): UUID of the user

        Returns:
            Any | None: The user object if exists
        """

        query = user_table \
            .select() \
            .where(user_table.c.id == uuid)

        user = await database.fetch_one(query)

        return user

    async def get_by_email(self, email: str) -> Any | None:
        """The method getting user by email

        Args:
            email (str): The email of the user

        Returns:
            Any | None: The user object if exists
        """

        query = user_table \
            .select() \
            .where(user_table.c.email == email)

        user = await database.fetch_one(query)

        return user