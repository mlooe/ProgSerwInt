"""Model containing tag-related domain models"""

from pydantic import BaseModel, ConfigDict


class TagIn(BaseModel):
    """Model representing all tags attributes"""
    name: str


class Tag(TagIn):
    """Model representing tags attributes in the database"""
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")