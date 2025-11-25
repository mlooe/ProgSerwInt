"""A module containing DTO models for review"""
from typing import Iterable

from pydantic import BaseModel, ConfigDict, UUID4, Optional  # type: ignore

class ReviewDTO(BaseModel):
    """A model representing DTO for review data"""
    id: int
    comic_id: int
    user_id: UUID4
    rating: int
    comment: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )