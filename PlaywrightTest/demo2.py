# async mode
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='msedge', headless=False)
        page = await browser.new_page()
        await page.goto('https://github.com/EightEggs')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='screenshot2.png')
        print(await page.title())
        await browser.close()

asyncio.run(main())
