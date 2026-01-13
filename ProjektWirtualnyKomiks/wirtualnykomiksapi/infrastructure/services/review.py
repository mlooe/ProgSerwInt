"""Module containing review service implementation"""

from typing import Iterable

from wirtualnykomiksapi.core.repositories.ireview import IReviewRepository
from wirtualnykomiksapi.core.domain.review import Review, ReviewIn
from wirtualnykomiksapi.infrastructure.dto.reviewdto import ReviewDTO
from wirtualnykomiksapi.infrastructure.services.ireview import IReviewService

class ReviewService(IReviewService):
    """A class implementing the review service"""

    _repository: IReviewRepository

    def __init__(self, repository: IReviewRepository) -> None:
        """The initializer of the 'review service'.

        Args:
            repository (IReviewRepository): The reference to the repository
        """

        self._repository = repository

    async def get_all_reviews(self) -> Iterable[ReviewDTO]:
        """The method getting all reviews from the repository.

        Returns:
            Iterable[ReviewDTO]: All reviews.
        """

        return await self._repository.get_all_reviews()

    async def get_review_by_user(self, user_id: str) -> Iterable[ReviewDTO]:
        """The method getting review by user id

        Args:
            user_id (str): The id of the user.

        Returns:
            Iterable[ReviewDTO]: The review details
        """

        return await self._repository.get_reviews_by_user(user_id)

    async def get_reviews_by_comic_id(self, comic_id: int) -> Iterable[ReviewDTO]:
        """The method getting reviews by comic id

        Args:
            comic_id (int): The id of the comic

        Returns:
            Iterable[ReviewDTO]: All the reviews for the given comic ID
        """

        return await self._repository.get_reviews_by_comic_id(comic_id)

    async def get_review_by_id(self, review_id: int) -> ReviewDTO | None:
        """The method getting review by id

        Args:
            review_id (int): The id of the review

        Returns:
            ReviewDTO | None: The review
        """

        return await self._repository.get_review_by_id(review_id)

    async def add_review(self, data: ReviewIn) -> Review | None:
        """The method adding new review to the data storage

        Args:
            data (ReviewIn): An input review

        Returns:
            Review | None: Full details of the newly added review
        """

        return await self._repository.add_review(data)

    async def update_review(self, review_id: int, data: ReviewIn) -> Review | None:
        """The method updating existing review in the data storage

        Args:
            review_id (int): The ID of the review
            data (ReviewIn): New data of the review

        Returns:
            Review | None: The updated review
        """

        return await self._repository.update_review(
            review_id=review_id,
            data=data,
        )

    async def delete_review(self, review_id: int) -> bool:
        """The method removing review with given id from the data storage

        Args:
            review_id (int): The ID of the review

        Returns:
            bool: Success of the operation
        """

        return await self._repository.delete_review(review_id)