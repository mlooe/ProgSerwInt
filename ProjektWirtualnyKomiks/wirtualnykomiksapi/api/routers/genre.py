"""A module containing genre-related routers"""
from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from wirtualnykomiksapi.container import Container
from wirtualnykomiksapi.core.domain.genre import Genre, GenreIn
from wirtualnykomiksapi.infrastructure.dto.genredto import GenreDTO
from wirtualnykomiksapi.infrastructure.services.igenre import IGenreService

router = APIRouter()

@router.get("/all", response_model=Iterable[GenreDTO], status_code=200)
@inject
async def get_all_genres(
        service: IGenreService = Depends(Provide[Container.genre_service]),
) -> Iterable:
    """An endpoint for getting all genres

    Args:
        service (IGenreService, optional): The injected service dependency

    Returns:
        Iterable: The genre attributes collection
    """

    genres = await service.get_all_genres()
    return genres


@router.get("/{genre_id}", response_model=GenreDTO, status_code=200)
@inject
async def get_genre_by_id(
        genre_id: int,
        service: IGenreService = Depends(Provide[Container.genre_service]),
) -> dict | None:
    """An endpoint for getting genre by id

    Args:
        genre_id (int): The id of the genre
        service (IGenreService, optional): The injected service dependency

    Returns:
        dict | None: The requested genre attributes
    """

    if genre := await service.get_genre_by_id(genre_id):
        return genre.model_dump()

    raise HTTPException(status_code=404, detail="Genre not found")


@router.post("/create", response_model=Genre, status_code=201)
@inject
async def create_genre(
        genre: GenreIn,
        service: IGenreService = Depends(Provide[Container.genre_service]),
) -> dict:
    """An endpoint for adding new genre

    Args:
        genre (GenreIn): The genre data
        service (IGenreService, optional): The injected service dependency

    Returns:
        dict: The new genre attributes
    """
    new_genre = await service.add_genre(genre)
    return new_genre.model_dump() if new_genre else {}


@router.put("/{genre_id}", response_model=Genre, status_code=201)
@inject
async def update_genre(
        genre_id: int,
        updated_genre: GenreIn,
        service: IGenreService = Depends(Provide[Container.genre_service]),
) -> dict:
    """An endpoint for updating genre data

    Args:
        genre_id (int): The id of the genre
        updated_genre (GenreIn): The updated genre details
        service (IGenreService, optional): The injected service dependency

    Raises:
         HTTPException: 404 if genre does not exist

    Returns:
        dict: The updated genre data
    """
    if await service.get_genre_by_id(genre_id=genre_id):
        new_updated_genre = await service.update_genre(
            genre_id=genre_id,
            data=updated_genre,
        )

        return new_updated_genre.model_dump() if new_updated_genre else {}

    raise HTTPException(status_code=404, detail="Genre not found")


@router.delete("/{genre_id}", status_code=204)
@inject
async def delete_genre(
        genre_id: int,
        service: IGenreService = Depends(Provide[Container.genre_service]),
) -> None:
    """An endpoint for deleting genres

    Args:
        genre_id (int): The id of the genre
        service (IGenreService, optional): The injected service dependency

    Raises:
        HTTPException: 404 if genre doesn't exist
    """

    if await service.get_genre_by_id(genre_id=genre_id):
        await service.delete_genre(genre_id)

        return

    raise HTTPException(status_code=404, detail="Genre not found")