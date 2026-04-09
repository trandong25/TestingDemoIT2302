from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service(executable_path='../../.venv/chromedriver.exe')

driver = webdriver.Chrome(service = service)
driver.get('https://vnexpress.net/')

acticles = driver.find_elements(By.CSS_SELECTOR, '#automation_TV0 > article')

for acticle in acticles:
    try:
        title = acticle.find_element(By.TAG_NAME, 'h3')
        des = acticle.find_element(By.CLASS_NAME, 'description')
        img = acticle.find_element(By.CSS_SELECTOR, 'div > a > picture > img')
        print(title.text)
        print(des.text)
        print(img.get_attribute('src'))
        title.click()
        normal = driver.find_element(By.CSS_SELECTOR, '#fck_detail_gallery > p')
        print(normal.text)
        print('=============')
    except NoSuchElementException as ex:
        pass

driver.quit()