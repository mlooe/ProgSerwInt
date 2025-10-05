import asyncio

async def korutyna1() -> None:
    await asyncio.sleep(3)
    print("To korutyna 1")


async def korutyna2() -> None:
    await asyncio.sleep(1)
    print("To korutyna 2")


async def main() -> None:
    await korutyna1()
    await korutyna2()

if __name__ == "__main__":
    asyncio.run(main())