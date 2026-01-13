"""Module providing containers injecting dependencies"""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from wirtualnykomiksapi.infrastructure.repositories.comicdb import ComicRepository
from wirtualnykomiksapi.infrastructure.repositories.reviewdb import ReviewRepository
from wirtualnykomiksapi.infrastructure.repositories.genredb import GenreRepository
from wirtualnykomiksapi.infrastructure.repositories.tagdb import TagRepository
from wirtualnykomiksapi.infrastructure.repositories.user_comic_listdb import UserComicListRepository
from wirtualnykomiksapi.infrastructure.repositories.user import UserRepository


from wirtualnykomiksapi.infrastructure.services.comic import ComicService
from wirtualnykomiksapi.infrastructure.services.review import ReviewService
from wirtualnykomiksapi.infrastructure.services.genre import GenreService
from wirtualnykomiksapi.infrastructure.services.tag import TagService
from wirtualnykomiksapi.infrastructure.services.user_comic_list import UserComicListService
from wirtualnykomiksapi.infrastructure.services.user import UserService

class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes"""
    comic_repository = Singleton(ComicRepository)
    review_repository = Singleton(ReviewRepository)
    genre_repository = Singleton(GenreRepository)
    tag_repository = Singleton(TagRepository)
    user_comic_list_repository = Singleton(UserComicListRepository)
    user_repository = Singleton(UserRepository)

    comic_service = Factory(
        ComicService,
        repository=comic_repository,
    )

    review_service = Factory(
        ReviewService,
        repository=review_repository,
    )

    genre_service = Factory(
        GenreService,
        repository=genre_repository,
    )

    tag_service = Factory(
        TagService,
        repository=tag_repository,
    )

    user_comic_list_service = Factory(
        UserComicListService,
        repository=user_comic_list_repository,
    )

    user_service = Factory(
        UserService,
        repository=user_repository,
    )
