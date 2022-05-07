# from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import json
import aiohttp
import logging
from os import makedirs
from os.path import exists


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://spa5.scrape.center/api/book/?limit={limit}&offset={offset}'
DETAIL_URL = 'https://spa5.scrape.center/api/book/{id}'
LIMIT = 18
TOTAL_PAGE = 1
CONCURRENCY = 20
RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)
# MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
# MONGO_DB_NAME = 'books'
# MONGO_COLLECTION_NAME = 'books'

# client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
# db = client[MONGO_DB_NAME]
# collection = db[MONGO_COLLECTION_NAME]

session = None
semaphore = asyncio.Semaphore(CONCURRENCY)


async def scrape_api(url):
    async with semaphore:
        try:
            logging.info('scraping %s', url)
            async with session.get(url) as response:
                response = await response.json()
                await asyncio.sleep(20)
                # You need to wait 20s for session safely closing!
                # But this is too long... how to deal with this?
            return response
        except aiohttp.ClientError:
            logging.error('error occurred while scraping %s',
                          url, exc_info=True)


async def scrape_index(page):
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    return await scrape_api(url)


async def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    data = await scrape_api(url)
    await save_data(data)


# async def save_data(data):
#     logging.info('saving data %s', data)
#     if data:
#         return await collection.update_one({
#             'id': data.get('id')
#         }, {
#             '$set': data
#         }, upsert=True)
async def save_data(data):
    # logging.info('saving data %s', data)
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)


async def main():
    # index tasks
    global session
    session = aiohttp.ClientSession()
    async with session:
        scrape_index_tasks = [asyncio.create_task(
            scrape_index(page)) for page in range(1, TOTAL_PAGE + 1)]
        results = await asyncio.gather(*scrape_index_tasks)

    # detail tasks
    ids = []
    for index_data in results:
        if not index_data:
            continue
        for item in index_data.get('results'):
            ids.append(item.get('id'))
    scrape_detail_tasks = [asyncio.create_task(
        scrape_detail(id)) for id in ids]
    await asyncio.wait(scrape_detail_tasks)

if __name__ == '__main__':

    asyncio.run(main())
