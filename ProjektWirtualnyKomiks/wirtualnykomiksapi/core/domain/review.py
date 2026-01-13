"""Model containing review-related domain models"""
from typing import Optional

from pydantic import BaseModel, ConfigDict, UUID4, Field


class ReviewIn(BaseModel):
    """Model representing all review's attributes"""
    comic_id: int
    rating: int = Field(default=1, ge=1, le=10, description="Rating of the review")
    comment: Optional[str] = None


class ReviewBroker(ReviewIn):
    """A broker class including user in the model"""
    user_id: UUID4

class Review(ReviewBroker):
    """Model representing review's attributes in the database"""
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")