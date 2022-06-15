# Intro

> https://playwright.dev/python/docs/intro

Playwright is a framework for Web Testing and Automation.

It allows testing `Chromium`, `Firefox` and `WebKit` with a single API.

Playwright is built to enable cross-browser web automation that is ever-green, capable, reliable and fast.

## Usage

Once installed, you can import Playwright in a Python script, and launch any of the 3 browsers (`chromium`, `firefox` and `webkit`).

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://playwright.dev")
    print(page.title())
    browser.close()
```

Playwright supports two variations of the API: `synchronous` and `asynchronous`. If your modern project uses `asyncio`, you should use async API:

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://playwright.dev")
        print(await page.title())
        await browser.close()

asyncio.run(main())
```
