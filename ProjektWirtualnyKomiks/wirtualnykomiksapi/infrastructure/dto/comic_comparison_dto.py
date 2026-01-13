"""A module containing DTO models for comic comparison"""

from pydantic import BaseModel, ConfigDict

class ComicComparisonDTO(BaseModel):
    """A model representing DTO for comic comparison"""
    comic1: int
    comic2: int
    views_diff: int
    likes_diff: int
    description_diff: bool

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )
