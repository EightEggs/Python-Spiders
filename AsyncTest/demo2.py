import time
import asyncio
import aiohttp


def test(request_number: int):
    start = time.time()

    async def get(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                await response.text()
        # Wait 100 ms for the underlying SSL connections to close
        await asyncio.sleep(0.1)
        return response

    async def request():
        url = 'https://www.bilibili.com/'
        await get(url)

    async def main():
        tasks = [asyncio.create_task(request()) for _ in range(request_number)]
        await asyncio.gather(*tasks)

    asyncio.run(main())

    end = time.time()
    print(request_number, 'Finished in %.2f seconds.' % (end - start))


if __name__ == '__main__':
    for n in [5, 10, 20, 50, 100, 200]:
        test(n)

#------- A possible output -------#
#|  5 Finished in 0.75 seconds.  |#
#| 20 Finished in 0.75 seconds.  |#
#| 50 Finished in 0.78 seconds.  |#
#|100 Finished in 0.82 seconds.  |#
#|200 Finished in 1.02 seconds.  |#
#---------------------------------#
