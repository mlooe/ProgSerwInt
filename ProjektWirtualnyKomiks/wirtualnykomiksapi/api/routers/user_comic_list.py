"""A module containing user comic list-related routers"""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from wirtualnykomiksapi.container import Container
from wirtualnykomiksapi.core.domain.user_comic_list import UserComicList, UserComicListBroker, UserComicListStatus
from wirtualnykomiksapi.infrastructure.dto.user_comic_listdto import UserComicListDTO
from wirtualnykomiksapi.infrastructure.services.iuser_comic_list import IUserComicListService
from wirtualnykomiksapi.infrastructure.utils import consts


bearer_scheme = HTTPBearer()

router = APIRouter()


@router.get("/all", response_model=Iterable[UserComicListDTO], status_code=200)
@inject
async def get_user_list(
        service: IUserComicListService = Depends(Provide[Container.user_comic_list_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Iterable:
    """An endpoint for getting user's comic list

    Args:
        service (IUserComicListService, optional): The injected service
        credentials (HTTPAuthorizationCredentials, optional): The credentials

    Returns:
        Iterable: The collection of comics in user's list
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

    comic_list = await service.get_user_list(user_id=user_uuid)
    return comic_list


@router.post("/add", response_model=UserComicList, status_code=201)
@inject
async def add_comic(
    comic_id: int,
    service: IUserComicListService = Depends(Provide[Container.user_comic_list_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for adding comic to user's comic list

    Args:
        comic_id (int): The id of the comic
        service (IUserComicListService, optional): The injected service dependency
        credentials (HTTPAuthorizationCredentials, optional): The credentials

    Returns:
        dict: The new comic list
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

    extended_user_list = UserComicListBroker(
        user_id=user_uuid,
        comic_id=comic_id,
        status=UserComicListStatus.PLANNING,
    )

    new_comic = await service.add_comic(extended_user_list)

    return new_comic.model_dump() if new_comic else {}


@router.put("/{comic_id}", response_model=UserComicList, status_code=201)
@inject
async def update_status(
        comic_id: int,
        status: str,
        service: IUserComicListService = Depends(Provide[Container.user_comic_list_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> UserComicListDTO:
    """An endpoint for updating comic status on user's list

    Args:
        comic_id (int): The id of the comic
        status (str): Status of the comic
        service (IUserComicListService, optional): The injected service dependency
        credentials (HTTPAuthorizationCredentials, optional): The credentials

    Raises:
        HTTPException: 404 if comic does not exist

    Returns:
        dict: The updated comic status details
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

    try:
        updated = await service.update_status(user_id=user_uuid, comic_id=comic_id, status=status)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


    if not updated:
        raise HTTPException(status_code=404, detail="Comic not found")

    return updated


@router.delete("/{comic_id}", status_code=204)
@inject
async def delete_comic(
        comic_id: int,
        service: IUserComicListService = Depends(Provide[Container.user_comic_list_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    """An endpoint for deleting comic from user's list

    Args:
        comic_id (int): The id of the comic
        service (IUserComicListService, optional): The  injected service
        credentials (HTTPAuthorizationCredentials, optional): The credentials

    Raises:
        HTTPException: 404 if comic doesn't exist in user's list
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

    delete = await service.delete_comic(user_id=user_uuid, comic_id=comic_id)

    if not delete:
        raise HTTPException(status_code=404, detail="Comic not found")

    return