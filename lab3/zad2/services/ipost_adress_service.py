from abc import ABC
from typing import Iterable

class IPostAdressService(ABC):
    async def load_data(self):
        pass

    async def filter(self, text: str) -> Iterable:
        pass

    async def sort_by_usage(self) -> Iterable:
        pass

    async def cleanup(self, seconds: int):
        pass