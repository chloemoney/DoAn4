from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BasePage:
    def __init__(self, driver, timeout=12):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def input_text(self, locator, text):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)
        return el


class AddCartPage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, "#inputSearchAuto")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".col-md-3.col-sm-6.col-xs-6.pro-loop")
    ADD_TO_CART = (By.CSS_SELECTOR, "#add-to-cart")
    TOAST_MESSAGE = (By.CSS_SELECTOR,"div.header_dropdown_content.site_cart p.titlebox")

    def search_product(self, keyword):
        el = self.input_text(self.SEARCH_INPUT, keyword)
        el.send_keys(Keys.ENTER)
        time.sleep(2)

    def open_first_product(self):
        items = self.wait.until(EC.presence_of_all_elements_located(self.SEARCH_RESULTS))
        if not items:
            raise AssertionError("❌ Không tìm thấy sản phẩm nào sau khi tìm kiếm!")
        items[0].click()  # ✅ click vào sản phẩm đầu tiên

    def add_to_cart(self):
        self.click(self.ADD_TO_CART)

    def get_toast_message(self, timeout=8):
        try:
            el = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.TOAST_MESSAGE)
            )
            return el.text.strip()
        except:
            return ""
