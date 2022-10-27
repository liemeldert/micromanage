import asyncio


async def printHello():
    await asyncio.sleep(1)  # do something
    print('hello')


async def printGoodbye():
    await asyncio.sleep(2)    # do something
    print('goodbye')


async def main():
    taskHello = asyncio.create_task(printHello())
    taskGoodbye = asyncio.create_task(printGoodbye())
    await taskHello
    await taskGoodbye

asyncio.run(main())
