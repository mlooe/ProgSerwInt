"""Module containing comic repository implementation."""

from typing import Any, Iterable, Optional, List

import sqlalchemy
from asyncpg import Record # type: ignore
from sqlalchemy import select, func, insert

from wirtualnykomiksapi.core.repositories.icomic import IComicRepository
from wirtualnykomiksapi.core.domain.comic import Comic, ComicBroker
from wirtualnykomiksapi.core.domain.genre import Genre
from wirtualnykomiksapi.core.domain.tag import Tag
from wirtualnykomiksapi.infrastructure.dto.comicdto import ComicDTO
from wirtualnykomiksapi.infrastructure.dto.comic_comparison_dto import ComicComparisonDTO

from wirtualnykomiksapi.db import (
    database,
    comic_table,
    review_table,
    genre_table,
    tag_table,
    comic_genre_table,
    comic_tag_table,
)

class ComicRepository(IComicRepository):
    """A class representing comic DB repository"""

    async def get_all_comics(self) -> Iterable[Any]:
        """The method getting all comics from the data storage.

            Returns:
                Iterable[Any]: Comics in the data storage.
        """

        avg_rating = func.coalesce(func.avg(review_table.c.rating), 0.0).label("average_rating")

        query = (
            select(
                comic_table,
                avg_rating
            )
            .select_from(comic_table.outerjoin(review_table))
            .order_by(comic_table.c.id)
            .group_by(comic_table.c.id)
        )
        comics = await database.fetch_all(query)
        return await self._connect_relations(comics)

    async def get_comic_by_id(self, comic_id: int) -> Any | None:
        """The method getting comic by provided id

        Args:
            comic_id (int): The id of the comic

        Returns:
            Any | None: The comic details
        """

        avg_rating = func.coalesce(func.avg(review_table.c.rating), 0.0).label("average_rating")

        query = (
            select(
                comic_table,
                avg_rating
            )
            .select_from(comic_table.outerjoin(review_table))
            .where(comic_table.c.id == comic_id)
            .group_by(comic_table.c.id)
        )
        comic = await database.fetch_one(query)

        if comic:
            result = await self._connect_relations([comic])
            return result[0] if result else None

        return None

    async def get_filtered_comics(self, genres: Optional[str], tags: Optional[str]) -> Iterable[Any]:
        """The method getting filtered collection of comics

        Args:
            genres (Optional[str]): The list of genres
            tags (Optional[str]): The list of tags

        Returns:
            Iterable[Any]: The filtered collection of comics
        """

        avg_rating = func.coalesce(func.avg(review_table.c.rating), 0.0).label("average_rating")
        query = select(comic_table, avg_rating)

        filtered_table = comic_table

        if genres:
            genre_list = [g.strip() for g in genres.split(',')]
            filtered_table = filtered_table.join(comic_genre_table).join(genre_table)
            query = query.where(
                sqlalchemy.or_(*[genre_table.c.name.ilike(f"%{g}%") for g in genre_list])
            )

        if tags:
            tag_list = [t.strip() for t in tags.split(',')]
            filtered_table = filtered_table.join(comic_tag_table).join(tag_table)
            query = query.where(
                sqlalchemy.or_(*[tag_table.c.name.ilike(f"%{t}%") for t in tag_list])
            )

        filtered_table = filtered_table.outerjoin(review_table, comic_table.c.id == review_table.c.comic_id)

        query = query.select_from(filtered_table).group_by(comic_table.c.id)
        
        comics = await database.fetch_all(query)

        return await self._connect_relations(comics)


    async def get_top_rated_comics(self, limit: int) -> Iterable[Any]:
        """The method getting comics with the highest average rating

        Args:
            limit (int): The amount of shown comics

        Returns:
            Iterable[Any]: The collection of highest average rated comics
        """

        avg_rating = func.coalesce(func.avg(review_table.c.rating), 0.0).label("average_rating")

        query = (
            select(
                comic_table.c.id,
                comic_table.c.title,
                comic_table.c.author,
                comic_table.c.description,
                comic_table.c.likes,
                comic_table.c.views,
                comic_table.c.user_id,
                avg_rating
            )

            .select_from(comic_table.outerjoin(review_table))
            .group_by(comic_table.c.id)
            .order_by(sqlalchemy.desc(avg_rating))
            .limit(limit)
        )
        comics = await database.fetch_all(query)
        return await self._connect_relations(comics)

    async def get_most_popular_comics(self, limit: int) -> Iterable[Any]:
        """The method getting comics with the most views

        Args:
            limit (int): The amount of shown comics

        Returns:
            Iterable[Any]: The collection of most viewed comics
        """

        avg_rating = func.coalesce(func.avg(review_table.c.rating), 0.0).label("average_rating")

        query = (
            select(
                comic_table.c.id,
                comic_table.c.title,
                comic_table.c.author,
                comic_table.c.description,
                comic_table.c.likes,
                comic_table.c.views,
                comic_table.c.user_id,
                avg_rating
            )

            .select_from(comic_table.outerjoin(review_table))
            .group_by(comic_table.c.id)
            .order_by(sqlalchemy.desc(comic_table.c.views))
            .limit(limit)
        )
        comics = await database.fetch_all(query)
        return await self._connect_relations(comics)

    async def compare_comics(self, comic_id1: int, comic_id2: int) -> Any | None:
        """The method comparing comics

        Args:
            comic_id1 (int): The id of the first comic
            comic_id2 (int): The id of the second comic

        Returns:
            Any | None: The compared comics details
        """
        comic1 = comic_table.alias("comic1")
        comic2 = comic_table.alias("comic2")

        query = (
            select(
                comic1.c.id.label("comic1"),
                comic2.c.id.label("comic2"),
                func.abs(comic1.c.views - comic2.c.views).label("views_diff"),
                func.abs(comic1.c.likes - comic2.c.likes).label("likes_diff"),
                (comic1.c.description == comic2.c.description).label("description_diff")
            )
            .where(comic1.c.id == comic_id1)
            .where(comic2.c.id == comic_id2)
        )

        result = await database.fetch_one(query)
        return ComicComparisonDTO(**dict(result)) if result else None

    async def add_comic(self, comic: ComicBroker) -> Any | None:
        """The method adding new comic to the data storage

        Args:
            comic (ComicBroker): An input comic

        Returns:
            Any | None: The comic report
        """

        comic_insert = (
            insert(comic_table)
            .values(
                title=comic.title,
                description=comic.description,
                author=comic.author,
                likes=comic.likes,
                views=comic.views,
                user_id=comic.user_id,
            )
            .returning(comic_table.c.id)
        )

        comic_id = await database.execute(comic_insert)

        for genre_id in comic.genres:
            await database.execute(
                insert(comic_genre_table).values(
                    comic_id=comic_id,
                    genre_id=genre_id,
                )
            )
        for tag_id in comic.tags:
            await database.execute(
                insert(comic_tag_table).values(
                    comic_id=comic_id,
                    tag_id=tag_id,
                )
            )

        return await self.get_comic_by_id(comic_id)

    async def update_comic(self, comic_id: int, data: ComicBroker) -> Any | None:
        """The method updating existing comic in the data storage

        Args:
            comic_id (int): The ID of the comic we want to update
            data (ComicBroker): New data of the comic

        Returns:
            Comic | None: The updated comic
        """

        if self._get_by_id(comic_id):
            comic_data = data.model_dump()
            genres = comic_data.pop('genres', [])
            tags = comic_data.pop('tags', [])

            query = (
                comic_table.update()
                .where(comic_table.c.id == comic_id)
                .values(**comic_data)
            )
            await database.execute(query)

            await database.execute(
                comic_genre_table.delete().where(comic_genre_table.c.comic_id == comic_id)
            )
            for genre_id in genres:
                await database.execute(
                    insert(comic_genre_table).values(
                        comic_id=comic_id,
                        genre_id=genre_id,
                    )
                )

            await database.execute(
                comic_tag_table.delete().where(comic_tag_table.c.comic_id == comic_id)
            )
            for tag_id in tags:
                await database.execute(
                    insert(comic_tag_table).values(
                        comic_id=comic_id,
                        tag_id=tag_id,
                    )
                )

            return await self.get_comic_by_id(comic_id)

        return None

    async def delete_comic(self, comic_id: int) -> bool:
        """Abstract method deleting comic with given id from the data storage

        Args:
            comic_id (int): The ID of the comic

        Returns:
            bool: Success of the operation
        """

        if self._get_by_id(comic_id):
            await database.execute(
                comic_genre_table.delete().where(comic_genre_table.c.comic_id == comic_id)
            )

            await database.execute(
                comic_tag_table.delete().where(comic_tag_table.c.comic_id == comic_id)
            )

            await database.execute(
                review_table.delete().where(review_table.c.comic_id == comic_id)
            )
            query = comic_table \
                .delete() \
                .where(comic_table.c.id == comic_id)

            await database.execute(query)
            return True
        return False


    async def _get_by_id(self, comic_id: int) -> Record | None:
        """A private method getting comic from the database based on its id

        Args:
            comic_id (int): The id of the comic

        Returns:
            Record | None: Comic record if it exists
        """
        query = (
            comic_table.select()
            .where(comic_table.c.id == comic_id)
            .order_by(comic_table.c.id)
        )
        return await database.fetch_one(query)


    async def _connect_relations(self, comics: List[Record]) -> List[ComicDTO]:
        """A private method for comic and genre/tag relations

        Args:
            comics (List[Record]): The list of comic records

        Returns:
            List[ComicDTO]: The comic with added relation
        """
        if not comics:
            return []

        comic_ids = [comic['id'] for comic in comics]

        genres_query = (
            select(genre_table, comic_genre_table.c.comic_id)
            .join(comic_genre_table)
            .where(comic_genre_table.c.comic_id.in_(comic_ids))
        )
        genres_rows = await database.fetch_all(genres_query)
        genres_map = {}
        for row in genres_rows:
            genres_map.setdefault(row['comic_id'], []).append(Genre(**dict(row)))

        tags_query = (
            select(tag_table, comic_tag_table.c.comic_id)
            .join(comic_tag_table)
            .where(comic_tag_table.c.comic_id.in_(comic_ids))
        )
        tags_rows = await database.fetch_all(tags_query)
        tags_map = {}
        for row in tags_rows:
            tags_map.setdefault(row['comic_id'], []).append(Tag(**dict(row)))

        result = []
        for comic in comics:
            c_dict = dict(comic)
            c_dict['genres'] = genres_map.get(comic['id'], [])
            c_dict['tags'] = tags_map.get(comic['id'], [])
            result.append(ComicDTO(**c_dict))

        return result