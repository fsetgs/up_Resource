# python 源码
import asyncio
import time

async def say_after(what):
    # await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after('hello')
    #await say_after(1, 'hello')执行完之后，才继续向下执行
    await say_after('world')

    print(f"finished at {time.strftime('%X')}")

print("开始")
asyncio.run(main())
print("结束")
