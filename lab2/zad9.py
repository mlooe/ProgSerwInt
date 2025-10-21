import aiohttp
import asyncio

async def send_request(url: str, data: dict) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            status = response.status
            if 200 <= status < 300:
                print("Sukces")
                return await response.json()
            elif 500 <= status < 600:
                print("Error serwera")
                await asyncio.sleep(1)
            else:
                print("Error klienta")
                return None               # do dokończenia



async def main() -> None:
    url = "https://restful-api.dev/"
    # idk

if __name__ == "__main__":
    asyncio.run(main())