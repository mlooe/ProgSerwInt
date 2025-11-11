"""Model containing review repository abstractions"""

from abc import ABC, abstractmethod
from typing import Iterable

from core.domains.review import Review, ReviewIn

class IReviewRepository(ABC):
    """An abstract class representing protocol of review repository"""

    @abstractmethod
    async def get_all_reviews(self) -> Iterable[Review]:
        """Abstract method retrieving all reviews from the data storage"""

    @abstractmethod
    async def get_review_by_id(self, review_id: int) -> Review | None:
        """Abstract method getting review by given id from the data storage"""

    @abstractmethod
    async def get_review_by_comic_id(self, comic_id: int) -> Iterable[Review]:
        """Abstract method getting reviews by given comic id from the data storage"""

    @abstractmethod
    async def get_review_by_user(self, user_id: int) -> Iterable[Review]:
        """Abstract method getting reviews by given user id from the data storage"""

    @abstractmethod
    async def get_average_rating(self, comic_id: int) -> float:
        """Abstract method getting average reviews rating for a comic"""

    @abstractmethod
    async def get_comic_ranking(self, limit: int = 10) -> Iterable[dict]:
        """Abstract method getting top 10 best comics"""

    @abstractmethod
    async def add_review(self, review: ReviewIn) -> None:
        """Abstract method adding new review to the data storage"""

    @abstractmethod
    async def update_review(self, review_id: int, data: ReviewIn) -> Review | None:
        """Abstract method updating existing comic in the data storage"""

    @abstractmethod
    async def delete_review(self, review_id: int) -> bool:
        """Abstract method deleting review with given id from the data storage"""