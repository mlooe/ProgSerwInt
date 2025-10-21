import aiohttp
import asyncio

async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()



async def main(path: str) -> None:
    url = "https://static.wikitide.net/italianbrainrotwiki/f/fa/Tung_tung_tung_sahur.png"
    download = await fetch(url)

    with open(path, 'wb') as f:
        f.write(download)

if __name__ == "__main__":
    path = "C:/Users/Wiktor/Pictures/sahur.png"
    asyncio.run(main(path))
