"""Module containing review service abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable


from wirtualnykomiksapi.core.domain.review import Review, ReviewIn
from wirtualnykomiksapi.infrastructure.dto.reviewdto import ReviewDTO

class IReviewService(ABC):
    """A class representing review repository"""

    @abstractmethod
    async def get_all_reviews(self) -> Iterable[ReviewDTO]:
        """The method getting all reviews from the repository

        Returns:
            Iterable[Review]: All reviews
        """

    @abstractmethod
    async def get_review_by_user(self, user_id: str) -> Iterable[Review]:
        """The method getting reviews assigned to user

        Args:
            user_id (str): The id of the user

        Returns:
            Iterable[Any]: The reviews of the user
        """

    @abstractmethod
    async def get_reviews_by_comic_id(self, comic_id: int) -> Iterable[ReviewDTO]:
        """The method getting reviews by comic id

        Args:
            comic_id (int): The id of the comic

        Returns:
            Iterable[ReviewDTO]: All the reviews for the given comic ID
        """

    @abstractmethod
    async def get_review_by_id(self, review_id: int) -> ReviewDTO | None:
        """The method getting review by id

        Args:
            review_id (int): The id of the review

        Returns:
            ReviewDTO | None: The review
        """

    @abstractmethod
    async def add_review(self, review: ReviewIn) -> Review | None:
        """The method adding new review to the data storage

        Args:
            review (ReviewIn): An input review

        Returns:
            Review: The review
        """

    @abstractmethod
    async def update_review(self, review_id: int, data: ReviewIn) -> Review | None:
        """The method updating review in the data storage

        Args:
            review_id (int): The ID of review we want to update
            data (ReviewIn): New data of the review

        Returns:
            Review | None: The updated review
        """

    @abstractmethod
    async def delete_review(self, review_id: int) -> bool:
        """The method removing review with given id from the data storage

        Args:
            review_id (int): The id of review

        Returns:
            bool: Success of the operation
        """