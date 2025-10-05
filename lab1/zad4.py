import asyncio

async def main() -> None:
    i = 1
    while i < 6:
        await asyncio.sleep(1)
        print(i)
        i+=1


if __name__ == "__main__":
    asyncio.run(main())