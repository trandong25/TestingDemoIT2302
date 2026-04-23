from eapp.test.page.HomePage import HomePage
from eapp.test.page.LoginPage import LoginPage
from eapp.test.test_base import driver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def test_search_product(driver):
    home = HomePage(driver=driver)
    kw = 'iPad'
    home.open_page()
    home.search(kw)
    # search = driver.find_element(By.CSS_SELECTOR, '#collapsibleNavbar > form > input')
    # search.send_keys(kw)
    # btn = driver.find_element(By.CSS_SELECTOR, '#collapsibleNavbar > form > button')
    # btn.click()


    time.sleep(1)

    results = driver.find_elements(By.CSS_SELECTOR,'.container .card-title')

    print(results)

    for r in results:
        assert kw in r.text

def test_login_from_cart(driver):
    login = LoginPage(driver)
    login.open_page(url='http://127.0.0.1:5000/login?next=/cart')
    login.login('admin','123456')

    time.sleep(2)

    assert driver.current_url == 'http://127.0.0.1:5000/cart'

    e = driver.find_element(By.CSS_SELECTOR,'#collapsibleNavbar > ul > li:nth-child(5) > a')

    assert 'admin' in e.text

def test_add_to_cart(driver):
    home = HomePage(driver)
    home.open_page()
    home.add_to_cart()

    e = driver.find_element(By.CLASS_NAME,'cart-counter')
    assert int(e.text) == 3