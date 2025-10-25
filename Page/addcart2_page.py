import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # ========== LOCATORS ==========
        self.SEARCH_BOX = (By.CSS_SELECTOR, "#inputSearchAuto")  # Ô tìm kiếm sản phẩm
        self.FIRST_PRODUCT = (By.CSS_SELECTOR, ".col-md-3.col-sm-6.col-xs-6.pro-loop")  # Sản phẩm đầu tiên
        self.INCREASE_BTN = (By.CSS_SELECTOR, "input[value='+']")  # Nút tăng số lượng
        self.DECREASE_BTN = (By.CSS_SELECTOR, "button[class='qtyminus qty-btn']")  # Nút giảm số lượng
        self.ADD_TO_CART_BTN = (By.CSS_SELECTOR, "#add-to-cart")  # Thêm giỏ hàng
        self.VIEW_CART_BTN = (By.CSS_SELECTOR, ".linktocart.button.dark")  # Xem giỏ hàng
        self.CART_QTY_INPUT = (By.CSS_SELECTOR, "#updates_1158922632")  # Ô số lượng
        self.REMOVE_PRODUCT_BTN = (By.CSS_SELECTOR, "tbody tr:nth-child(1) td:nth-child(3) a:nth-child(1) img:nth-child(1)")  # Xóa sản phẩm
        self.EMPTY_CART_MSG = (By.CSS_SELECTOR,".expanded_message")

    # ========== PAGE ACTIONS ==========
    def open_homepage(self, url="https://swe.vn/"):
        """Mở trang chủ"""
        self.driver.get(url)

    def search_product(self, keyword):
        """Nhập từ khóa vào ô tìm kiếm"""
        box = self.wait.until(EC.presence_of_element_located(self.SEARCH_BOX))
        box.clear()
        box.send_keys(keyword)
        box.submit()
        time.sleep(2)

    def open_first_product(self):
        """Nhấn vào sản phẩm đầu tiên"""
        first = self.wait.until(EC.element_to_be_clickable(self.FIRST_PRODUCT))
        first.click()
        time.sleep(2)

    def increase_quantity(self, times=1):
        """Nhấn nút '+' nhiều lần"""
        btn = self.wait.until(EC.element_to_be_clickable(self.INCREASE_BTN))
        for _ in range(times):
            btn.click()
            time.sleep(0.5)

    def decrease_quantity(self, times=1):
        """Nhấn nút '-' nhiều lần"""
        btn = self.wait.until(EC.element_to_be_clickable(self.DECREASE_BTN))
        for _ in range(times):
            btn.click()
            time.sleep(0.5)

    def add_to_cart(self):
        """Nhấn nút 'Thêm vào giỏ hàng'"""
        btn = self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BTN))
        btn.click()
        time.sleep(2)

    def view_cart(self):
        """Nhấn 'Xem giỏ hàng'"""
        btn = self.wait.until(EC.element_to_be_clickable(self.VIEW_CART_BTN))
        btn.click()
        time.sleep(2)

    def get_cart_quantity(self):
        """Lấy số lượng sản phẩm trong giỏ"""
        qty = self.wait.until(EC.presence_of_element_located(self.CART_QTY_INPUT))
        return int(qty.get_attribute("value"))

    def remove_product(self):
        """Xóa sản phẩm khỏi giỏ hàng"""
        remove = self.wait.until(EC.element_to_be_clickable(self.REMOVE_PRODUCT_BTN))
        remove.click()
        time.sleep(2)

    def is_cart_empty(self):
        """Kiểm tra giỏ hàng có trống không"""
        try:
            empty_msg = self.wait.until(EC.visibility_of_element_located(self.EMPTY_CART_MSG))
            return empty_msg.is_displayed()
        except:
            return False
