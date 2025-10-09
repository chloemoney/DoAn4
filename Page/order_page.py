import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OrderPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)
        self.driver.maximize_window()

    def click(self, by, locator):
        self.wait.until(EC.element_to_be_clickable((by, locator))).click()

    def input_text(self, by, locator, text, submit=False):
        el = self.wait.until(EC.visibility_of_element_located((by, locator)))
        el.clear()
        el.send_keys(text)
        if submit:
            el.submit()
        return el

    def get_text(self, by, locator, timeout=8):
        try:
            el = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
            return el.text.strip()
        except:
            return ""

    # ====== Functional actions ======
    def search_product(self, keyword):
        self.input_text(By.CSS_SELECTOR, "#inputSearchAuto", keyword, submit=True)
        time.sleep(2)
    def click_first_result(self):
        self.click(By.CSS_SELECTOR, ".col-md-3.col-sm-6.col-xs-6.pro-loop")
    def increase_quantity(self, quantity):
        try:
            plus = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[value='+']")
            ))
            for _ in range(int(quantity) - 1):
                plus.click()
                time.sleep(0.4)
        except:
            print("Không tìm thấy nút '+' hoặc sản phẩm chỉ có 1 lựa chọn.")

    def add_to_cart(self):
        self.click(By.CSS_SELECTOR, "#add-to-cart")

    def view_cart(self):
        self.click(By.CSS_SELECTOR, ".linktocart.button.dark")

    def get_cart_message(self):
        return self.get_text(By.CSS_SELECTOR, "div[class='header-page'] h1")
