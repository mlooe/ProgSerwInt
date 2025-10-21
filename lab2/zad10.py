import aiohttp
import asyncio


async def fetch(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def process(data: dict) -> str:
    proccessed = []
    for item in data:
        name = item.get("name", "nie ma nazwy")
        proccessed.append(name)

    result = ""

    for name in proccessed:
        result += name + "\n"

    return result


async def main(path: str) -> None:
    url = "https://68e6851b21dd31f22cc5ffad.mockapi.io/api/v1/user"

    data = await fetch(url)
    proccessed_data = await process(data)

    with open(path, 'w', encoding="utf-8") as f:
        f.write(proccessed_data)


if __name__ == "__main__":
    path = "C:/Users/Wiktor/Documents/plik1.txt"
    asyncio.run(main(path))