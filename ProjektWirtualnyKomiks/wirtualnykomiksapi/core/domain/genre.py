"""Model containing genre domain models"""

from pydantic import BaseModel, ConfigDict

class GenreIn(BaseModel):
    """Model representing all genre attributes"""
    name: str

class Genre(GenreIn):
    """Model representing genre's attributes in the database"""
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")