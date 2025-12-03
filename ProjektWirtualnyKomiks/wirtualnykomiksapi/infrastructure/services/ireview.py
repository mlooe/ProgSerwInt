"""Module containing review service abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable, Optional, List

from ProjektWirtualnyKomiks.wirtualnykomiksapi.core.domain.review import Review, ReviewIn
from ProjektWirtualnyKomiks.wirtualnykomiksapi.infrastructure.dto.reviewdto import ReviewDTO
from pydantic import UUID4


class IReviewService(ABC):
    """A class representing review repository"""

    @abstractmethod
    async def get_all_reviews(self) -> Iterable[ReviewDTO]:
        """The method retrieving all reviews from the data storage

        Returns:
            Iterable[ReviewDTO]: All the reviews
        """

    @abstractmethod
    async def get_review_by_id(self, review_id: int) -> ReviewDTO | None:
        """The method getting review by given id from the data storage

        Args:
            review_id(int): The ID of the review

        Returns:
            ReviewDTO | None: The review with given ID
        """

    @abstractmethod
    async def get_reviews_by_user(self, user_id: UUID4) -> Iterable[Review]:
        """The method getting user reviews by given id from the data storage

        Args:
            user_id: The UUID of the user

        Returns:
            Iterable[Review]: The collection of reviews by given user ID
        """

    @abstractmethod
    async def get_reviews_by_comic_id(self, comic_id: int) -> Iterable[ReviewDTO]:
        """The method getting reviews by given comic id from the data storage

        Args:
            comic_id (int): The ID of the comic

        Returns:
            Iterable[ReviewDTO]: All the reviews for the given comic ID
        """

    @abstractmethod
    async def get_average_rating(self, comic_id: int) -> float:
        """The method getting average reviews rating for a comic

        Args:
            comic_id (int): The ID of the comic

        Returns:
            float: Average rating of the comic
        """

    @abstractmethod
    async def add_review(self, data: ReviewIn) -> Review:
        """The method adding new review to the data storage

        Args:
            data (ReviewIn): An input comic

        Returns:
            Review: The review
        """

    @abstractmethod
    async def update_review(self, review_id: int, data: ReviewIn) -> Review | None:
        """The method updating existing comic in the data storage

        Args:
            review_id (int): The ID of the review
            data (ReviewIn): New data of the review

        Returns:
            Review | None: The updated review
        """

    @abstractmethod
    async def delete_review(self, review_id: int) -> bool:
        """The method deleting review with given id from the data storage

        Args:
            review_id (int): The ID of the review

        Returns:
            bool: Success of the operation
        """

