"""Model containing comic-related domain models"""

from pydantic import BaseModel, ConfigDict
from typing import List

from core.domain.genre import Genre
from core.domain.tag import Tag


class ComicIn(BaseModel):
    """Model representing all comic's attributes"""
    title: str
    description: str
    author: str
    genres: List[Genre] = []
    tags: List[Tag] = []

class Comic(ComicIn):
    """Model representing comic's attributes in the database"""
    id: int
    likes: int = 0
    views: int = 0
    average_rating: float = 0.0
    model_config = ConfigDict(from_attributes=True, extra="ignore")
