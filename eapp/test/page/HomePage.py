from selenium.webdriver.common.by import By
from eapp.test.page.BasePage import BasePage


class HomePage(BasePage):
    URL = 'http://127.0.0.1:5000/'

    SEARCH_INPUT = (By.CSS_SELECTOR, '#collapsibleNavbar > form > input')
    SEARCH_BUTTON = (By.CSS_SELECTOR, '#collapsibleNavbar > form > button')
    PRODUCT_BUTTON1 = (By.CSS_SELECTOR,'.container div:nth-child(1) > div > div > button')
    PRODUCT_BUTTON2 = (By.CSS_SELECTOR,'.container div:nth-child(2) > div > div > button')
    CART_COUNTET = (By.CLASS_NAME, 'cart-counter')

    def open_page(self):
        self.open(self.URL)

    def search(self, kw):
        self.typing(*self.SEARCH_INPUT,kw)
        self.click(*self.SEARCH_BUTTON)

    def add_to_cart(self):
        self.click(*self.PRODUCT_BUTTON1)
        self.driver.implicitly_wait(2)
        self.click(*self.PRODUCT_BUTTON1)
        self.driver.implicitly_wait(2)
        self.click(*self.PRODUCT_BUTTON2)


