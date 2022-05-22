from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Edge()
try:
    browser.get('https://baidu.com/')
    input_area = browser.find_element(By.ID, 'kw')
    input_area.send_keys('Python')
    input_area.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    print(browser.current_url)
finally:
    browser.quit()
