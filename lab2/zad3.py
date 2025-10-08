import aiohttp
import asyncio

async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        

async def main() -> None:
    url1 = "https://uwm.edu.pl/"
    url2 = "https://www.gov.pl/"
    url3 = "https://allegro.pl/"
    url4 = "https://moodle.org/"
    url5 = "https://github.com/"

    urls = await asyncio.gather(fetch(url1), fetch(url2), fetch(url3), fetch(url4), fetch(url5))
    
    print(urls)
    

if __name__ == "__main__":
    asyncio.run(main())