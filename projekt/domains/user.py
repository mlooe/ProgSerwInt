"""Model containing user-related domain models"""

from typing import Iterable
from pydantic import BaseModel, ConfigDict

class UserIn(BaseModel):
    """Model representing all user's attributes"""
    username: str
    password: str
    planned: Iterable[str]
    reading: Iterable[str]
    dropped: Iterable[str]

class User(UserIn):
    """Model representing all user's attributes in the database"""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")