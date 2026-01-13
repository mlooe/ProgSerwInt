"""A module containing tag-related routers"""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import HTTPBearer


from wirtualnykomiksapi.container import Container
from wirtualnykomiksapi.core.domain.tag import Tag, TagIn
from wirtualnykomiksapi.infrastructure.dto.tagdto import TagDTO
from wirtualnykomiksapi.infrastructure.services.itag import ITagService

bearer_scheme = HTTPBearer()

router = APIRouter()

@router.get("/all", response_model=Iterable[TagDTO], status_code=200)
@inject
async def get_all_tags(
        service: ITagService = Depends(Provide[Container.tag_service]),
) -> Iterable:
    """An endpoint for getting all tags

    Args:
        service (ITagService, optional): The injected service dependency

    Returns:
        Iterable: The tag attributes collection
    """

    tags = await service.get_all_tags()
    return tags


@router.get("/{tag_id}", response_model=TagDTO, status_code=200)
@inject
async def get_tag_by_id(
        tag_id: int,
        service: ITagService = Depends(Provide[Container.tag_service]),
) -> dict | None:
    """An endpoint for getting tag details by id

    Args:
        tag_id (int): The id of the tag
        service (ITagService, optional): The injected service dependency

    Raises:
        HTTPException: 404 if tag does not exist

    Returns:
        dict | None: The requested tag attributes
    """

    if tag := await service.get_tag_by_id(tag_id=tag_id):
        return tag.model_dump()

    raise HTTPException(status_code=404, detail="Tag not found")


@router.post("/create", response_model=Tag, status_code=201)
@inject
async def create_tag(
        tag: TagIn,
        service: ITagService = Depends(Provide[Container.tag_service]),
) -> dict:
    """An endpoint for adding new tags

    Args:
        tag (TagIn): The tag data
        service (ITagService, optional): The injected service dependency

    Returns:
        dict: The new tag attributes
    """

    new_tag = await service.add_tag(tag)

    return new_tag.model_dump() if new_tag else {}


@router.put("/{tag_id}", response_model=Tag, status_code=201)
@inject
async def update_tag(
        tag_id: int,
        updated_tag: TagIn,
        service: ITagService = Depends(Provide[Container.tag_service]),
) -> dict:
    """An endpoint for updating tag data

    Args:
        tag_id (int): The id of the tag
        updated_tag (TagIn): The updated tag details
        service (ITagService, optional): The injected service dependency

    Raises:
        HTTPException: 404 if tag does not exist

    Returns:
        dict: The updated tag data
    """
    if await service.get_tag_by_id(tag_id=tag_id):
        new_updated_tag = await service.update_tag(
            tag_id=tag_id,
            data=updated_tag,
        )

        return new_updated_tag.model_dump() if new_updated_tag else {}

    raise HTTPException(status_code=404, detail="Tag not found")


@router.delete("/{tag_id}", status_code=204)
@inject
async def delete_tag(
        tag_id: int,
        service: ITagService = Depends(Provide[Container.tag_service]),
) -> None:
    """An endpoint for deleting tags

    Args:
        tag_id (int): The id of the tag
        service (ITagService, optional):The injected service dependency

    Raises:
        HTTPException: 404 if tag doesn't exist
    """

    if await service.get_tag_by_id(tag_id=tag_id):
        await service.delete_tag(tag_id)

        return

    raise HTTPException(status_code=404, detail="Tag not found")