import asyncio

async def fibonacci() -> None:
    f_0 = 0
    f_1 = 1

    await asyncio.sleep(1)
    print(f_0)

    await asyncio.sleep(1)
    print(f_1)

    while True:             # nieskończona pętla
        f_n = f_0 + f_1             # f_n przechodzi do przodu (takie jakby i w pętli for)
        await asyncio.sleep(1)

        print(f_n)

        f_0 = f_1
        f_1 = f_n

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    task = loop.create_task(fibonacci())                # utworzenie obiektu, który się będzie wykonywał?

    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:               # kombinacja CTRL + C zamyka aplikacje 
        print("Zamknięcie aplikacji")

        tasks = asyncio.all_tasks(loop=loop)
        for task_ in tasks:
            task_.cancel()

        group = asyncio.gather(*tasks, return_exceptions=True)              # zgromadzenie i zgrupowanie zadań
        loop.run_until_complete(group)
        loop.close()
