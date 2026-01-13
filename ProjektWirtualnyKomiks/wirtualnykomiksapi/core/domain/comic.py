"""Model containing comic-related domain models"""

from pydantic import BaseModel, ConfigDict, UUID4, Field
from typing import List


class ComicIn(BaseModel):
    """Model representing all comic's attributes"""
    title: str
    description: str
    author: str
    likes: int = Field(default=0, ge=0, le=10000, description="Amount of likes for comic")
    views: int = Field(default=0, ge=0, le=1000000, description="Amount of views for comic")
    genres: List[int] = []
    tags: List[int] = []

class ComicBroker(ComicIn):
    """A broker class including user in the model"""
    user_id: UUID4

class Comic(ComicBroker):
    """Model representing comic's attributes in the database"""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
