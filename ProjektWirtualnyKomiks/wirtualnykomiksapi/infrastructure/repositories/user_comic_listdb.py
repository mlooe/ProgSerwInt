from typing import Iterable, Any, Optional

from sqlalchemy import select, join

from wirtualnykomiksapi.db import (
database,
user_comic_list_table,
comic_table
)

from wirtualnykomiksapi.core.repositories.iuser_comic_list import IUserComicListRepository
from wirtualnykomiksapi.core.domain.user_comic_list import UserComicList, UserComicListStatus

class UserComicListRepository(IUserComicListRepository):
    """A class representing user comic list DB repository"""

    async def get_user_list(self, user_id: str) -> Iterable[Any]:
        """The method getting user list

        Args:
            user_id (str): The user id

        Returns:
            Iterable[Any]: The user comic list
        """

        query = (
            select(user_comic_list_table, comic_table)
            .select_from(
                join(
                    user_comic_list_table,
                    comic_table,
                    user_comic_list_table.c.comic_id == comic_table.c.id
                )
            )
            .where(user_comic_list_table.c.user_id == user_id)
            .order_by(comic_table.c.title.asc())
        )
        comics = await database.fetch_all(query)
        return [UserComicList(**dict(comic)) for comic in comics]

    async def add_comic(self, user_id: str, comic_id: int) -> Any:
        """The method adding comic to user list

        Args:
            user_id (str): The user id
            comic_id (int): The id of the comic

        Returns:
            Any: The comic
        """

        query = user_comic_list_table.insert().values(
            user_id=user_id,
            comic_id=comic_id,
            status=UserComicListStatus.PLANNING.value
        )
        entry_id = await database.execute(query)
        record = await database.fetch_one(
            user_comic_list_table.select().where(user_comic_list_table.c.id == entry_id)
        )
        return UserComicList(**dict(record))

    async def update_status(self, user_id: str, comic_id: int, status: str) -> Optional[Any]:
        """The method updating status for comic

        Args:
            user_id (str): The user id
            comic_id (int): The id of the comic
            status (str): The status of the comic

        Returns:
            Optional[Any]: The user comic list
        """

        if await self._get_comic(user_id, comic_id):
            query = (
                user_comic_list_table.update()
                .where(
                    (user_comic_list_table.c.user_id == user_id) &
                    (user_comic_list_table.c.comic_id == comic_id)
                )
                .values(status=status)
            )
            await database.execute(query)
            record = await self._get_comic(user_id, comic_id)
            return UserComicList(**dict(record)) if record else None
        return None

    async def delete_comic(self, user_id: str, comic_id: int) -> bool:
        """The method deleting comic

        Args:
            user_id (str): The user id
            comic_id (int): The id of the comic

        Returns:
            bool: Success of the operation
        """

        if await self._get_comic(user_id, comic_id):
            query = user_comic_list_table.delete().where(
                (user_comic_list_table.c.user_id == user_id) &
                (user_comic_list_table.c.comic_id == comic_id)
            )
            await database.execute(query)
            return True
        return False

    async def _get_comic(self, user_id: str, comic_id: int) -> Optional[Any]:
        """A private method getting comic from the database based on its id

        Args:
            user_id (str): The id of the user
            comic_id (int): The id of the comic

        Returns:
            Optional[Any]: The comic
        """

        query = (
            user_comic_list_table.select()
            .where(
                (user_comic_list_table.c.user_id == user_id) &
                (user_comic_list_table.c.comic_id == comic_id)
            )
        )
        return await database.fetch_one(query)