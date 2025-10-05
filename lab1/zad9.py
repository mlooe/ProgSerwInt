import asyncio

async def maszyna_A():
    czas_działania = 0
    while czas_działania < 15:
        await asyncio.sleep(2)
        print("maszyna A pracuje")
        czas_działania+=2
    

async def maszyna_B():
    czas_działania = 0
    while czas_działania < 15:
        await asyncio.sleep(3)
        print("maszyna B pracuje")
        czas_działania+=3

async def maszyna_C():
    czas_działania = 0
    while czas_działania < 15:
        await asyncio.sleep(5)
        print("maszyna C pracuje")
        czas_działania+=5

async def main():
    maszyny = [maszyna_A(), maszyna_B(), maszyna_C()]
    await asyncio.gather(*maszyny)              # zamiast pętli zdarzeń można użyć tego

if __name__ == "__main__":
    asyncio.run(main())
