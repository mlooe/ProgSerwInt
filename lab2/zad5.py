import aiohttp
import asyncio

async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def main() -> None:
    Porlamar = "https://api.open-meteo.com/v1/forecast?latitude=10.9577&longitude=-63.8697&hourly=temperature_2m,relative_humidity_2m,visibility,showers,wind_speed_10m&timezone=auto&forecast_days=1"
    Moroni = "https://api.open-meteo.com/v1/forecast?latitude=-11.7022&longitude=43.2551&hourly=temperature_2m,relative_humidity_2m,visibility,showers,wind_speed_10m&timezone=auto&forecast_days=1"
    Helsinek = "https://api.open-meteo.com/v1/forecast?latitude=60.1695&longitude=24.9354&hourly=temperature_2m,relative_humidity_2m,visibility,showers,wind_speed_10m&timezone=auto&forecast_days=1"

    urls = await asyncio.gather(fetch(Porlamar), fetch(Moroni), fetch(Helsinek))

    print("Porlamar: ", urls[0]["hourly"])
    print("Moroni: ", urls[1]["hourly"])
    print("Helsinek: ", urls[2]["hourly"])

if __name__ == "__main__":
    asyncio.run(main())