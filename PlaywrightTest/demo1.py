# sync mode
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=False)
    page = browser.new_page()
    page.goto('https://www.github.com/')
    page.wait_for_timeout(2000)
    page.screenshot(path='screenshot1.png')
    print(page.title())
    browser.close()
