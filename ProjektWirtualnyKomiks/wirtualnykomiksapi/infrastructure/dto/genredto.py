"""A module containing DTO models for genre"""

from pydantic import BaseModel, ConfigDict  # type: ignore

class GenreDTO(BaseModel):
    """A model representing DTO for genre data"""
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )