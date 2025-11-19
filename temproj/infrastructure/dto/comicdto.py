"""A module containing DTO models for comic."""
from typing import Iterable

from pydantic import BaseModel, ConfigDict  # type: ignore

from core.domains.comic import Comic

class ComicDTO(BaseModel):
    """A model representing DTO for comic data."""
    id: int
    title: str
    description: str
    likes: int = 0
    views: int = 0
    genres: Iterable[str]
    tags: Iterable[str]

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )