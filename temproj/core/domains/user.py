"""Model containing user-related domain models"""

from typing import Iterable
from pydantic import BaseModel, ConfigDict

class UserIn(BaseModel):
    """Model representing all user's attributes"""
    username: str
    email: str
    password: str
    to_read: Iterable[str] = []
    paused: Iterable[str] = []
    abandoned: Iterable[str] = []

class User(UserIn):
    """Model representing all user's attributes in the database"""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
