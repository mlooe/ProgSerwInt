from dependency_injector import containers, providers

from repositories.post_adress_repository import PostAdressRepository
from services.post_adress_service import PostAdressService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    repository = providers.Singleton(
        PostAdressRepository
    )

    service = providers.Factory(
        PostAdressService,
        repository=repository,
    )