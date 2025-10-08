import aiohttp
import asyncio

async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        

async def main() -> None:
    url = "https://uwm.edu.pl/"
    users = await fetch(url)

    print(users)

if __name__ == "__main__":
    asyncio.run(main())
    