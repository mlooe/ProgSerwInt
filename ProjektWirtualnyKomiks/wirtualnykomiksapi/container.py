"""Module providing containers injecting dependencies"""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from wirtualnykomiksapi.infrastructure.repositories.comicdb import ComicRepository
from wirtualnykomiksapi.infrastructure.services.comic import ComicService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    comic_repository = Singleton(ComicRepository)

    comic_service = Factory(
        ComicService,
        repository=comic_repository,
    )