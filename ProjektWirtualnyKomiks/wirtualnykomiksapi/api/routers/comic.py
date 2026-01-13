"""A module containing comic-related routers"""

from typing import Iterable, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from wirtualnykomiksapi.container import Container
from wirtualnykomiksapi.core.domain.comic import ComicIn, ComicBroker
from wirtualnykomiksapi.infrastructure.dto.comicdto import ComicDTO
from wirtualnykomiksapi.infrastructure.dto.comic_comparison_dto import ComicComparisonDTO
from wirtualnykomiksapi.infrastructure.services.icomic import IComicService
from wirtualnykomiksapi.infrastructure.utils import consts

bearer_scheme = HTTPBearer()

router = APIRouter()


@router.get("/all", response_model=Iterable[ComicDTO], status_code=200)
@inject
async def get_all_comics(
        service: IComicService = Depends(Provide[Container.comic_service]),#type: ignore
) -> Iterable:
    """An endpoint for getting all comics

    Args:
        service (IComicService, optional): The injected service dependency

    Returns:
        Iterable: The comics attributes collection
    """

    comics = await service.get_all_comics()

    return comics


@router.get("/id/{comic_id}", response_model=ComicDTO, status_code=200)
@inject
async def get_comic_by_id(
        comic_id: int,
        service: IComicService = Depends(Provide[Container.comic_service]),
) -> dict | None:
    """An endpoint for comic by id

    Args:
        comic_id (int): The id of the comic
        service (IComicService, optional): The injected service dependency

    Returns:
        dict | None: The comic details
    """

    if comic := await service.get_comic_by_id(comic_id):
        return comic.model_dump()

    raise HTTPException(status_code=404, detail="Comic not found")


@router.get("/filter", response_model=Iterable[ComicDTO], status_code=200)
@inject
async def get_filtered_comics(
    genres: Optional[str] = None,
    tags: Optional[str] = None,
    service: IComicService = Depends(Provide[Container.comic_service]),
) -> Iterable:
    """An endpoint for getting filtered comics

    Args:
        genres (Optional[str]): The genre
        tags (Optional[str]): The tag
        service (IComicService, optional): The injected service dependency

    Returns:
        Iterable: The comics details collection
    """

    comics = await service.get_filtered_comics(genres=genres, tags=tags)
    return comics


@router.get("/top-rated", response_model=Iterable[ComicDTO], status_code=200)
@inject
async def get_top_rated_comics(
        limit: int,
        service: IComicService = Depends(Provide[Container.comic_service]),
) -> Iterable:
    """An endpoint for getting comics with the highest average rating

    Args:
        limit (int): The amount of shown comics
        service (IComicService, optional): The injected service dependency

    Returns:
        Iterable: The comic collection of highest average rated comics
    """
    comics = await service.get_top_rated_comics(limit=limit)
    return comics


@router.get("/most-popular", response_model=Iterable[ComicDTO], status_code=200)
@inject
async def get_most_popular_comics(
        limit: int,
        service: IComicService = Depends(Provide[Container.comic_service]),
) -> Iterable:
    """An endpoint for getting comics with the most views

    Args:
        limit (int): The amount of shown comics
        service (IComicService, optional): The injected service dependency

    Returns:
        Iterable: The comic collection of most viewed comics
    """

    comics = await service.get_most_popular_comics(limit=limit)
    return comics


@router.get("/compare", response_model=ComicComparisonDTO, status_code=200)
@inject
async def compare_comics(
        comic_id1: int,
        comic_id2: int,
        service: IComicService = Depends(Provide[Container.comic_service]),
) -> dict:
    """An endpoint for comparing two comics

    Args:
        comic_id1 (int): The id of the first comic
        comic_id2 (int): The id of the second comic
        service (IComicService, optional): The injected service dependency

    Returns:
        dict: The comparison comic details
    """

    if comparison := await service.compare_comics(comic_id1, comic_id2):
        return comparison.model_dump()

    raise HTTPException(status_code=404, detail="One or both comics not found")


@router.post("/create", response_model=ComicDTO, status_code=201)
@inject
async def create_comic(
        comic: ComicIn,
        service: IComicService = Depends(Provide[Container.comic_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for adding new comic

    Args:
        comic (ComicIn): The comic data,
        service (IComicService, optional): The injected service dependency
        credentials (HTTPAuthorizationCredentials, optional): The credentials

    Returns:
        dict: The new comic attributes
    """
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    extended_comic_data = ComicBroker(
        user_id=user_uuid,
        **comic.model_dump()
    )
    new_comic = await service.add_comic(extended_comic_data)

    return new_comic.model_dump() if new_comic else {}


@router.put("/{comic_id}", response_model=ComicDTO, status_code=200)
@inject
async def update_comic(
        comic_id: int,
        updated_comic: ComicIn,
        service: IComicService = Depends(Provide[Container.comic_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating comic data

    Args:
        comic_id (int): The id of the comic
        updated_comic (ComicIn): The updated comic details
        service (IComicService, optional): The injected service dependency
        credentials (HTTPAuthorizationCredentials, optional): The crendetials

    Raises:
        HTTPException: 404 if comic doesn't exist

    Returns:
        dict: The updated comic details
    """
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if comic_data := await service.get_comic_by_id(comic_id=comic_id):
        if str(comic_data.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_updated_comic = ComicBroker(
            user_id=user_uuid,
            **updated_comic.model_dump(),
        )

        updated_comic_data = await service.update_comic(
            comic_id=comic_id,
            data=extended_updated_comic,
        )
        return updated_comic_data.model_dump() if updated_comic_data \
            else {}

    raise HTTPException(status_code=404, detail="Comic not found")


@router.delete("/{comic_id}", status_code=204)
@inject
async def delete_comic(
        comic_id: int,
        service: IComicService = Depends(Provide[Container.comic_service])
) -> None:
    """An endpoint for deleting comics

    Args:
        comic_id (int): The id of the comic
        service (IComicService, optional): The injected service dependency

    Raises:
        HTTPException: 404 if comic does not exist
    """
    if await service.get_comic_by_id(comic_id=comic_id):
        await service.delete_comic(comic_id)

        return

    raise HTTPException(status_code=404, detail="Comic not found")