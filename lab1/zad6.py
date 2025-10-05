import asyncio

async def fetch(delay: int):
    await asyncio.sleep(delay)
    return 67

async def main() -> None:
    fetch1 = await fetch(1)
    print(fetch1)

    fetch2 = await fetch(5)
    print(fetch2)

    fetch3 = await fetch(3)
    print(fetch3)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    task = loop.create_task(main())

    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        print("Zamknięcie aplikacji")

        tasks = asyncio.all_tasks(loop=loop)
        for task_ in tasks:
            task_.cancel()

        group = asyncio.gather(*tasks, return_exceptions=True)
        loop.run_until_complete(group)
        loop.close()
