"""A module containing DTO models for comic"""
from typing import Iterable

from pydantic import BaseModel, ConfigDict  # type: ignore

from ProjektWirtualnyKomiks.wirtualnykomiksapi.core.domain.genre import Genre
from ProjektWirtualnyKomiks.wirtualnykomiksapi.core.domain.tag import Tag

class ComicDTO(BaseModel):
    """A model representing DTO for comic data"""
    id: int
    title: str
    author: str
    description: str
    likes: int
    views: int
    average_rating: float = 0.0
    genres: Iterable[Genre] = []
    tags: Iterable[Tag] = []

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )