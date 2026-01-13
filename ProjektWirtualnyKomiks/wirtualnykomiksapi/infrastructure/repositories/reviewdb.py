"""Module containing review repository implementation."""

from typing import Any, Iterable
from sqlalchemy import select, func
from asyncpg import Record  # type: ignore

from wirtualnykomiksapi.core.repositories.ireview import IReviewRepository
from wirtualnykomiksapi.core.domain.review import Review, ReviewIn

from wirtualnykomiksapi.db import (
    database,
    review_table,
)

from wirtualnykomiksapi.infrastructure.dto.reviewdto import ReviewDTO

class ReviewRepository(IReviewRepository):
    """A class representing review DB repository"""

    async def get_all_reviews(self) -> Iterable[Any]:
        """The method getting all reviews from the data storage.

            Returns:
                Iterable[Any]: Reviews in the data storage.
        """
        query = (
            select(
                review_table
            )
            .order_by(review_table.c.id)
        )
        reviews = await database.fetch_all(query)
        return [ReviewDTO(**dict(review)) for review in reviews]

    async def get_reviews_by_user(self, user_id: str) -> Iterable[Any]:
        """The method getting user reviews by given id from the data storage

        Args:
            user_id (str): The id of the user

        Returns:
            Iterable[Any]: The collection of reviews by given user ID
        """

        query = (
            select(
                review_table.c.id,
                review_table.c.comic_id,
                review_table.c.user_id,
                review_table.c.rating,
                review_table.c.comment,
            )
            .where(review_table.c.user_id == user_id)
            .order_by(review_table.c.id.asc())
        )
        reviews = await database.fetch_all(query)
        return [ReviewDTO(**dict(review)) for review in reviews]

    async def get_review_by_id(self, review_id: int) -> Any | None:
        """The method getting review by given id from the data storage

        Args:
            review_id(int): The ID of the review

        Returns:
            Any | None: The review with given ID
        """

        review = await self._get_by_id(review_id)
        return Review(**dict(review)) if review else None

    async def get_reviews_by_comic_id(self, comic_id: int) -> Iterable[Any]:
        """The method getting reviews by given comic id from the data storage

        Args:
            comic_id (int): The ID of the comic

        Returns:
            Iterable[Any]: All the reviews for the given comic ID
        """

        query = (
            select(
                review_table.c.id,
                review_table.c.comic_id,
                review_table.c.user_id,
                review_table.c.rating,
                review_table.c.comment,
            )
            .where(review_table.c.comic_id == comic_id)
        )
        reviews = await database.fetch_all(query)

        return [ReviewDTO(**dict(review)) for review in reviews]

    async def get_average_rating(self, comic_id: int) -> float:
        """The method getting average reviews rating for a comic

        Args:
            comic_id (int): The ID of the comic

        Returns:
            float: Average rating of the comic

        """
        query = (
            select(
                func.avg(review_table.c.rating).label("average_rating")
            )
            .where(review_table.c.comic_id == comic_id)
        )
        rating = await database.fetch_one(query)

        return rating

    async def add_review(self, data: ReviewIn) -> Any | None:
        """The method adding new review to the data storage

        Args:
            data (ReviewIn): An input comic

        Returns:
            Any | None: The review
        """

        query = review_table.insert().values(**data.model_dump())
        new_review_id = await database.execute(query)
        new_review = await self._get_by_id(new_review_id)

        return Review(**dict(new_review) if new_review else None)

    async def update_review(self, review_id: int, data: ReviewIn) -> Any | None:
        """The method updating existing comic in the data storage

        Args:
            review_id (int): The ID of the review
            data (ReviewIn): New data of the review

        Returns:
            Any | None: The updated review
        """

        if self._get_by_id(review_id):
            query = (
                review_table.update()
                .where(review_table.c.id == review_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            review = await self._get_by_id(review_id)
            return Review(**dict(review)) if review else None
        return None

    async def delete_review(self, review_id: int) -> bool:
        """The method deleting review with given id from the data storage

        Args:
            review_id (int): The ID of the review

        Returns:
            bool: Success of the operation
        """

        if self._get_by_id(review_id):
            query = review_table \
                .delete() \
                .where(review_table.c.id == review_id)
            await database.execute(query)
            return True
        return False


    async def _get_by_id(self, review_id: int) -> Record | None:
        """A private method getting review from the database based on its id

        Args:
            review_id (int): The id of the review

        Returns:
            Record | None: Review record if it exists
        """
        query = (
            review_table.select()
            .where(review_table.c.id == review_id)
            .order_by(review_table.c.id)
        )
        return await database.fetch_one(query)