import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        # Trường tìm kiếm
        self.search_field = (By.ID, "inputSearchAuto")
        # Nút submit search
        self.search_button = (By.CSS_SELECTOR, "button.btn-search")
        # Kết quả tìm kiếm (nếu có sản phẩm)
        self.search_result_container = (By.CSS_SELECTOR, ".subtxt")
        # Kết quả khi không tìm thấy sản phẩm
        self.search_result_error = (By.CSS_SELECTOR, "div.expanded-message.text-center h2")


    def open(self, url):
        self.driver.get(url)

    def search(self, keyword):
        search_input = self.driver.find_element(*self.search_field)
        search_input.clear()
        if keyword:
            search_input.send_keys(keyword)

        self.driver.find_element(*self.search_button).click()
        time.sleep(2)

    def get_search_message(self):
        try:
            # Validation của input (nếu để trống)
            search_input = self.driver.find_element(*self.search_field)
            if search_input.get_attribute("validationMessage"):
                return search_input.get_attribute("validationMessage")

            # Kết quả hiển thị trên trang
            container_text = self.driver.find_element(*self.search_result_container).text
            return container_text.strip()

        except NoSuchElementException:
            return ""
