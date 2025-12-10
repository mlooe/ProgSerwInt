"""Model containing user comic list status domain models"""

from pydantic import BaseModel, ConfigDict, UUID4


class UserComicListStatus(str):
    """Comic status in user's comic list"""
    PLANNING = "planning"
    READING = "reading"
    COMPLETED = "completed"
    DROPPED = "dropped"


class UserComicListIn(BaseModel):
    """Model representing all user comic list attributes"""
    comic_id: int
    status: UserComicListStatus


class UserComicList(UserComicListIn):
    """Model representing user comic list attributes in the database"""
    id: int
    user_id: UUID4

    model_config = ConfigDict(from_attributes=True, extra="ignore")