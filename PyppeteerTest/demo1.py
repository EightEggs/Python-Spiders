import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'


async def main():
    browser = await launch(executablePath=PATH, headless=False)
    page = await browser.newPage()
    await page.goto('https://spa2.scrape.center/')
    await page.waitForSelector('.item .name')
    doc = pq(await page.content())
    names = [i.text() for i in doc('.item .name').items()]
    print(names)
    await browser.close()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
