import asyncio

async def wczytanie_pliku():
    await asyncio.sleep(2)
    print("Wczytywanie pliku...")

async def analiza_pliku():
    await asyncio.sleep(4)
    print("Analizowanie pliku...")

async def zapisywanie_pliku():
    await asyncio.sleep(1)
    print("Zapisywanie pliku...")


async def main():
    await wczytanie_pliku()
    await analiza_pliku()
    await zapisywanie_pliku()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    task = loop.create_task(main())

    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        print("Zamknięcie aplikacji...")

        tasks = asyncio.all_tasks(loop=loop)
        for task_ in tasks:
            task_.cancel()

        group = asyncio.gather(*tasks, return_exceptions=True)
        loop.run_until_complete(group)
        loop.close()