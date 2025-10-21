import aiohttp
import asyncio


async def fetch(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()



async def main() -> None:
    urls = {
        "Porlamar": "https://api.open-meteo.com/v1/forecast?latitude=10.9577&longitude=-63.8697&hourly=temperature_2m&timezone=auto&forecast_days=1",
        "Moroni": "https://api.open-meteo.com/v1/forecast?latitude=-11.7022&longitude=43.2551&hourly=temperature_2m&timezone=auto&forecast_days=1",
        "Helsinki": "https://api.open-meteo.com/v1/forecast?latitude=60.1695&longitude=24.9354&hourly=temperature_2m&timezone=auto&forecast_days=1",
    }

    results = await asyncio.gather(*(fetch(url) for url in urls.values()))              # asynchronicznie pobiera dane

    avg_temps = {}


    for city, data in zip(urls.keys(), results):
        temps = data["hourly"]["temperature_2m"]
        average = sum(temps) / len(temps)
        avg_temps[city] = average

    final_tab = dict(sorted(avg_temps.items(), key=lambda kv: kv[1], reverse=True))

    print(final_tab)

if __name__ == "__main__":
    asyncio.run(main())