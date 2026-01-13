"""A module containing DTO models for tags"""

from pydantic import BaseModel, ConfigDict  # type: ignore

class TagDTO(BaseModel):
    """A model representing DTO for tags data"""
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )