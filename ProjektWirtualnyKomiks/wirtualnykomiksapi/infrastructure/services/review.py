"""Module containing review service implementation"""

from typing import Iterable, Optional, List

from wirtualnykomiksapi.core.domain.review import Review, ReviewBroker
from wirtualnykomiksapi.core.repositories.ireview import IReviewRepository
from wirtualnykomiksapi.infrastructure.services.ireview import IReviewService
from wirtualnykomiksapi.infrastructure.dto.reviewdto import ReviewDTO
from pydantic import UUID4


class ReviewService(IReviewService):
    """A class implementing the review service."""

    _repository: IReviewRepository

    def __init__(self, repository: IReviewRepository) -> None:
        """The initializer of the review service.

        Args:
            repository (IReviewService): The reference to the repository.
        """

        self._repository = repository

    async def get_all_reviews(self) -> Iterable[ReviewDTO]:
        """The method retrieving all reviews from the data storage

        Returns:
            Iterable[ReviewDTO]: All the reviews
        """

        return await self._repository.get_all_reviews()

    async def get_review_by_id(self, review_id: int) -> ReviewDTO | None:
        """The method getting review by given id from the data storage

        Args:
            review_id(int): The ID of the review

        Returns:
            ReviewDTO | None: The review with given ID
        """

        return await self._repository.get_review_by_id(review_id)

    async def get_reviews_by_user(self, user_id: UUID4) -> Iterable[Review]:
        """The method getting user reviews by given id from the data storage

        Args:
            user_id: The UUID of the user

        Returns:
            Iterable[Review]: The collection of reviews by given user ID
        """

        return await self._repository.get_reviews_by_user(user_id)

    async def get_reviews_by_comic_id(self, comic_id: int) -> Iterable[ReviewDTO]:
        """The method getting reviews by given comic id from the data storage

        Args:
            comic_id (int): The ID of the comic

        Returns:
            Iterable[ReviewDTO]: All the reviews for the given comic ID
        """

        return await self._repository.get_reviews_by_comic_id(comic_id)

    async def get_average_rating(self, comic_id: int) -> float:
        """The method getting average reviews rating for a comic

        Args:
            comic_id (int): The ID of the comic

        Returns:
            float: Average rating of the comic
        """

        return await self._repository.get_average_rating(comic_id)

    async def add_review(self, data: ReviewBroker) -> Review | None:
        """The method adding new review to the data storage

        Args:
            data (ReviewBroker): The details of the new review

        Returns:
            Review | None: Full details of the newly added review
        """

        return await self._repository.add_review(data)

    async def update_review(self, review_id: int, data: ReviewBroker) -> Review | None:
        """The method updating existing comic in the data storage

        Args:
            review_id (int): The ID of the review
            data (ReviewBroker): The details of the updated review

        Returns:
            Review | None: The updated review details
        """

        return await self._repository.update_review(review_id=review_id, data=data)

    async def delete_review(self, review_id: int) -> bool:
        """The method deleting review with given id from the data storage

        Args:
            review_id (int): The ID of the review

        Returns:
            bool: Success of the operation
        """

        return await self._repository.delete_review(review_id)
