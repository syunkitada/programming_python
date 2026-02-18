import asyncio

class AsyncContextManager:
    async def __aenter__(self):
        print("Entering the async context")
        await asyncio.sleep(1)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        print("Exiting the async context")
        await asyncio.sleep(1)

async def main():
    async with AsyncContextManager() as acm:
        print("Inside the async context")

asyncio.run(main())