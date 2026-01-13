"""Model containing user comic list status domain models"""

from pydantic import BaseModel, ConfigDict, UUID4
from enum import Enum

class UserComicListStatus(str, Enum):
    """Comic status in user's comic list"""
    PLANNING = "planning"
    READING = "reading"
    COMPLETED = "completed"
    DROPPED = "dropped"


class UserComicListIn(BaseModel):
    """Model representing all user comic list attributes"""
    comic_id: int
    status: UserComicListStatus

class UserComicListBroker(UserComicListIn):
    """A broker class including user in the model"""
    user_id: UUID4

class UserComicList(UserComicListBroker):
    """Model representing user comic list attributes in the database"""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore", arbitrary_types_allowed=True)