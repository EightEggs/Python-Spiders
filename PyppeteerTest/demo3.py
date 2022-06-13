import asyncio
from pyppeteer import launch

PATH = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
WIDTH, HEIGHT = 1200, 800


async def main():
    browser = await launch(executablePath=PATH, headless=False,
                           userDataDir='D:\\Projects\\Python Spiders\\PyppeteerTest\\.userdata',
                           args=['--disable-infobars', f'--window-size={WIDTH},{HEIGHT}'])
    page = await browser.newPage()
    await page.setViewport({'width': WIDTH, 'height': HEIGHT})
    # bypass anti-webdriver detection
    await page.evaluateOnNewDocument('''Object.defineProperty(
        navigator, "webdriver", {get: ()=>undefined})''')
    await page.goto('https://taobao.com/')
    await asyncio.sleep(10)
    await browser.close()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
