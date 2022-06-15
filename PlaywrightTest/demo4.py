# route
import asyncio
import re
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='msedge', headless=False)
        page = await browser.new_page()
        await page.route(re.compile(r"(\.png)|(\.jpg)"), lambda r: r.abort())
        await page.goto('https://bilibili.com/')
        await page.wait_for_load_state('networkidle')
        await page.screenshot(path='routed.png')
        await browser.close()

asyncio.run(main())
