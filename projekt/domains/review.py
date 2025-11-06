"""Model containing review-related domain models"""

from pydantic import BaseModel, ConfigDict



class ReviewIn(BaseModel):
    """Model representing all review's attributes"""
    comic_id: int
    username: str
    text: str
    score: int

class Review(ReviewIn):
    """Model representing review's attributes in the database"""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
