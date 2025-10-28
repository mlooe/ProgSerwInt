import aiohttp
import asyncio

async def fetch(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def main() -> None:
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    pogoda = await fetch(url)

    czas = pogoda["hourly"]["time"][0]
    temperatura = pogoda["hourly"]["temperature_2m"][0]
    wilgotnosc = pogoda["hourly"]["relative_humidity_2m"][0]
    wiatr = pogoda["hourly"]["wind_speed_10m"][0]

    print("Zakopane prognoza ", czas)
    print("Temperatura: ", temperatura)
    print("Wilgotnosc: ", wilgotnosc)
    print("Wiatr: ", wiatr)

if __name__ == "__main__":
    asyncio.run(main())