import asyncio
from contextlib import aclosing

async def async_generator():
    print("generator: start")
    try:
        for i in range(5):
            print(f"generator: yielding {i}")
            yield i
            await asyncio.sleep(0.5)
    finally:
        # aclose() が呼ばれるとここが実行される
        print("generator: cleanup (finally block)")

async def main():
    async with aclosing(async_generator()) as gen:
        async for value in gen:
            print(f"consumer: got {value}")
            if value == 2:
                break  # 途中で抜けても cleanup が実行される

asyncio.run(main())