import asyncio

async def start_strongman(name, power, quantity=5):
    print(f"Силач {name} начал соревнования.")
    for number in range(0, quantity):
        await asyncio.sleep(5 / power)
        print(f"Силач {name} поднял {number + 1} шар" )
    print(f"Силач {name} закончил соревнования.")

async def start_tournament():
    task1 = asyncio.create_task(start_strongman('Pasha', 3))
    task2 = asyncio.create_task(start_strongman('Denis', 4))
    task3 = asyncio.create_task(start_strongman('Apollon', 5))
    await task1
    await task2
    await task3


if __name__ == "__main__":
    asyncio.run(start_tournament())

