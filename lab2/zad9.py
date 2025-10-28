import aiohttp
import asyncio

async def send_request(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if 200 <= response.status < 300:
                print("Sukces")
                return await response.json()
            elif 500 <= response.status < 600:
                print("Error serwera")
                await asyncio.sleep(1)
        return None



async def main() -> None:
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

    for i in range(100):
        pogoda = await send_request(url)
        print(pogoda)


if __name__ == "__main__":
    asyncio.run(main())