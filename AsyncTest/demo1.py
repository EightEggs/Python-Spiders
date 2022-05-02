import time
import asyncio
import aiohttp

start = time.time()


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            await response.text()
    # Wait 500 ms for the underlying SSL connections to close
    await asyncio.sleep(0.5)
    return response


async def request():
    url = "https://www.httpbin.org/delay/3"
    print('Waiting for', url)
    response = await get(url)
    print('Get response:', response.status)


async def main():
    tasks = [asyncio.create_task(request()) for _ in range(10)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
    end = time.time()
    print('Finished in %.2f seconds.' % (end - start))
