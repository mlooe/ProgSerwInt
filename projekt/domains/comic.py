"""Model containing comic-related domain models"""

from pydantic import BaseModel, ConfigDict
from typing import Iterable


class ComicIn(BaseModel):
    """Model representing all comic's attributes"""
    title: str
    description: str
    likes: int
    genres: Iterable[str]
    reviews: Iterable[str]

class Comic(ComicIn):
    """Model representing comic's attributes in the database"""
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")