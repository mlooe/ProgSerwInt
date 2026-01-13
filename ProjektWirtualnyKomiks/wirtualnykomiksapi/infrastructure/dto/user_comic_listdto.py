"""A module containing DTO models for user's comic list"""

from pydantic import BaseModel, ConfigDict, UUID4  # type: ignore
from enum import Enum

class UserComicListStatus(str, Enum):
    """Comic status in user's comic list"""
    PLANNING = "planning"
    READING = "reading"
    COMPLETED = "completed"
    DROPPED = "dropped"

class UserComicListDTO(BaseModel):
    """A model representing DTO for user comic list data"""
    id: int
    user_id: UUID4
    comic_id: int
    status: UserComicListStatus

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )