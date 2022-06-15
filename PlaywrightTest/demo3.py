# listener
import asyncio
from playwright.async_api import async_playwright


async def on_json_response(response):
    if '/api/movie' in response.url and response.status == 200:
        print(await response.json())


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='msedge', headless=False)
        page = await browser.new_page()
        page.on('response', on_json_response)
        await page.goto('https://spa6.scrape.center/')
        await page.wait_for_load_state('networkidle')
        await browser.close()

asyncio.run(main())
