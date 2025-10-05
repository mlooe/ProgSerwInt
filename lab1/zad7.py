import asyncio

async def krojenie_warzyw() -> None:
    await asyncio.sleep(2)
    print("Krojenie warzyw!")

async def gotowanie_makaronu() -> None:
    await asyncio.sleep(5)
    print("Gotowanie makaronu!")

async def smazenie_miesa() -> None:
    await asyncio.sleep(3)
    print("Smażenie mięsa!")

async def main() -> None:
    await krojenie_warzyw()
    await gotowanie_makaronu()
    await smazenie_miesa()



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