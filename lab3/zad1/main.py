from dependency_injector.wiring import Provide

import asyncio

from container import Container
from zad1.services.ipost_adress_service import IPostAdressService
from zad1.utils import consts

async def main(
        service: IPostAdressService = Provide[Container.service],

) -> None:
    await service.load_posts(consts.URL)
    result = await service.search("labore")

    for i in result:
        print(i)



if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    asyncio.run(main())