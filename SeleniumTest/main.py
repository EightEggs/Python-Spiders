from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

### Initialization ###
browser = webdriver.Edge()
# browser = webdriver.Chrome()
# browser= webdriver.Firefox()
# browser = webdriver.Safari()
# browser = webdriver.Opera()


### Request ###
browser.get("https://taobao.com")
time.sleep(3)
# with open('result.html', 'w', encoding='utf-8') as f:
#     f.write(browser.page_source)


### Find nodes ###
input_1 = browser.find_element(By.ID, 'q')
input_2 = browser.find_element(By.CSS_SELECTOR, '#q')
input_3 = browser.find_element(By.XPATH, '//*[@id="q"]')
print(input_1, input_2, input_3, sep='\n')

lis = browser.find_elements(By.CSS_SELECTOR, '.service-bd li')
for li in lis:
    print(li.text)


### Node Operations ###
input_1.send_keys('iPhone')
button = browser.find_element(By.CLASS_NAME, 'btn-search')
time.sleep(1)
button.click()
time.sleep(3)


### Action Chains ###
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to.frame('iframeResult')
begin = browser.find_element(By.CSS_SELECTOR, '#draggable')
target = browser.find_element(By.CSS_SELECTOR, '#droppable')
actions = ActionChains(browser)
actions.drag_and_drop(begin, target)
actions.perform()
time.sleep(3)


### Execute Script ###
url = 'https://zhihu.com/explore'
browser.get(url)
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("To bottom.")')
time.sleep(3)


### Get Attributes ###
url = 'https://spa2.scrape.center/'
browser.get(url)
logo = browser.find_element(By.CLASS_NAME, 'logo-image')
print(logo.get_attribute('src'))
print(logo.id)
print(logo.tag_name)
print(logo.location)
print(logo.size)
print(logo.text)


### Wait ###
# implicit wait
browser.implicitly_wait(5)
# explicit wait
input_1 = WebDriverWait(browser, 5).until(
    EC.presence_of_element_located((By.ID, 'q')))


### Forward and Backward###
browser.back()
browser.forward()


### Manage Pages ###
browser.execute_script('window.open()')
pages = browser.window_handles
print(pages)
browser.switch_to.window(pages[1])
browser.get('http://example.com/')
browser.switch_to.window(pages[0])


### Headless Mode ###
options = EdgeOptions()
options.add_argument('--headless')
browser = webdriver.Edge(options=options)
browser.set_window_size(1366, 768)
browser.get('https://baidu.com/')
browser.get_screenshot_as_file('screenshot.png')


### Anti-WebDriver ###
browser = webdriver.Edge()
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})
browser.get('https://antispider1.scrape.center/')
time.sleep(5)


### Quit ###
browser.quit()
