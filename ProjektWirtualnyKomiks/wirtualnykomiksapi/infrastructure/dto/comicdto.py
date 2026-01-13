"""A module containing DTO models for comic"""

from pydantic import BaseModel, ConfigDict, UUID4  # type: ignore
from typing import List

from wirtualnykomiksapi.core.domain.genre import Genre
from wirtualnykomiksapi.core.domain.tag import Tag

class ComicDTO(BaseModel):
    """A model representing DTO for comic data"""
    id: int
    title: str
    author: str
    description: str
    likes: int
    views: int
    user_id: UUID4
    average_rating: float = 0.0
    genres: List[Genre] = []
    tags: List[Tag] = []

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )