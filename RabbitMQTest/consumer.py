import pika
import aiohttp
import asyncio

MAX_PRIORITY = 100
QUEUE_NAME = 'scrape_queue'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

tasks = []


async def scrape(request):
    try:
        session = aiohttp.ClientSession()
        print(f'Scraping {request}...')
        response = await session.get(request)
        await session.close()
        await asyncio.sleep(0.75)
        return response
    except Exception as e:
        print(f'Error {e} occurred when scraping {request}.')

while True:
    method_frame, header, body = channel.basic_get(
        queue=QUEUE_NAME, auto_ack=True)
    if body:
        request = body.decode('utf-8')
        print(f'Get: {request}')
        task = scrape(request)
        tasks.append(task)
    else:
        break


async def main():

    results = await asyncio.gather(*tasks)
    for result in results:
        print(result.status)


asyncio.run(main())
