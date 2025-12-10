"""Model containing review repository abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable, Any
from pydantic import UUID4

from wirtualnykomiksapi.core.domain.review import ReviewIn


class IReviewRepository(ABC):
    """An abstract class representing protocol of review repository"""

    @abstractmethod
    async def get_all_reviews(self) -> Iterable[Any]:
        """Abstract method retrieving all reviews from the data storage

        Returns:
            Iterable[Any]: All the reviews
        """

    @abstractmethod
    async def get_review_by_id(self, review_id: int) -> Any | None:
        """Abstract method getting review by given id from the data storage

        Args:
            review_id(int): The ID of the review

        Returns:
            Any | None: The review with given ID
        """

    @abstractmethod
    async def get_reviews_by_user(self, user_id: UUID4) -> Iterable[Any]:
        """Abstract method getting user reviews by given id from the data storage

        Args:
            user_id: The UUID of the user

        Returns:
            Iterable[Any]: The collection of reviews by given user ID
        """

    @abstractmethod
    async def get_reviews_by_comic_id(self, comic_id: int) -> Iterable[Any]:
        """Abstract method getting reviews by given comic id from the data storage

        Args:
            comic_id (int): The ID of the comic

        Returns:
            Iterable[Any]: All the reviews for the given comic ID
        """


    @abstractmethod
    async def get_average_rating(self, comic_id: int) -> float:
        """Abstract method getting average reviews rating for a comic

        Args:
            comic_id (int): The ID of the comic

        Returns:
            float: Average rating of the comic

        """

    @abstractmethod
    async def add_review(self, data: ReviewIn) -> Any:
        """Abstract method adding new review to the data storage

        Args:
            data (ReviewIn): An input comic

        Returns:
            Any: The review
        """

    @abstractmethod
    async def update_review(self, review_id: int, data: ReviewIn) -> Any | None:
        """Abstract method updating existing comic in the data storage

        Args:
            review_id (int): The ID of the review
            data (ReviewIn): New data of the review

        Returns:
            Any | None: The updated review
        """

    @abstractmethod
    async def delete_review(self, review_id: int) -> bool:
        """Abstract method deleting review with given id from the data storage

        Args:
            review_id (int): The ID of the review

        Returns:
            bool: Success of the operation
        """