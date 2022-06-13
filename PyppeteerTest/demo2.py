import asyncio
from pyppeteer import launch

PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
WIDTH, HEIGHT = 1366, 768


async def main():
    browser = await launch(executablePath=PATH, headless=False)
    page = await browser.newPage()
    await page.setViewport({'width': WIDTH, 'height': HEIGHT})
    await page.goto('https://spa2.scrape.center/')
    await page.waitForSelector('.item .name')
    await asyncio.sleep(2)
    await page.screenshot(path='screenshot.png', omitBackground=True)
    info = await page.evaluate('''()=>{
        return {
            userAgent: window.navigator.userAgent,
            width: document.documentElement.clientWidth,
            heigth: document.documentElement.clientHeight
        }
    }
    ''')
    print(info)
    await browser.close()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
