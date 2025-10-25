import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # ====== INPUT LOCATORS (GIỮ NGUYÊN) ======
        self.NAME = (By.NAME, "name")
        self.PHONE = (By.NAME, "phone")
        self.EMAIL = (By.NAME, "email")
        self.PROVINCE = (By.NAME, "address")   # tên hơi sai nhưng giữ nguyên theo yêu cầu
        self.ADDRESS = (By.NAME, "fulladdress")
        self.SUBMIT_BTN = (By.ID, "place_order")

        # ====== BUTTON LOCATORS (GIỮ NGUYÊN) ======
        self.ADD_TO_CART = (By.CSS_SELECTOR, "#add-to-cart, button.add-to-cart")
        self.CHECKOUT_BTN = (By.CSS_SELECTOR, ".linktocheckout.button.red, a[href*='checkout']")

    # ================== HỖ TRỢ CƠ BẢN ==================
    def safe_click(self, locator):
        """Cuộn tới và click an toàn (tránh popup hoặc che khuất)."""
        el = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            el.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", el)
        time.sleep(1)

    def _type(self, locator, value):
        """Nhập dữ liệu an toàn vào ô input."""
        try:
            field = self.wait.until(EC.presence_of_element_located(locator))
            field.clear()
            if value:
                field.send_keys(value)
        except TimeoutException:
            print(f" Không tìm thấy field {locator}")

    # ================== LUỒNG NGHIỆP VỤ ==================
    def search_product(self, keyword):
        """Tìm kiếm sản phẩm theo từ khóa."""
        search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.submit()
        time.sleep(2)

    def click_first_product(self):
        """Mở sản phẩm đầu tiên trong danh sách kết quả."""
        self.safe_click((By.CSS_SELECTOR, ".product-block a, .product-item a"))
        time.sleep(2)

    def add_to_cart(self):
        """Click nút 'Thêm vào giỏ hàng'."""
        self.safe_click(self.ADD_TO_CART)
        time.sleep(1.5)

    def go_to_checkout_from_popup(self):
        """Từ popup giỏ hàng → tới trang checkout."""
        try:
            self.safe_click(self.CHECKOUT_BTN)
        except TimeoutException:
            print(" Popup không hiện → chuyển thẳng sang trang checkout.")
            self.driver.get("https://swe.vn/checkout")
        time.sleep(2)

    def fill_checkout_form(self, name, phone, email, province, address):
        """Điền thông tin vào form thanh toán."""
        self._type(self.NAME, name)
        self._type(self.PHONE, phone)
        self._type(self.EMAIL, email)
        self._type(self.PROVINCE, province)
        self._type(self.ADDRESS, address)
        time.sleep(1)

    def submit_order(self):
        """Nhấn nút 'Đặt hàng'."""
        self.safe_click(self.SUBMIT_BTN)
        time.sleep(2)

    # ================== LẤY THÔNG BÁO LỖI ==================
    def _get_error_by_text(self, keyword):
        """
        Tìm thông báo lỗi có chứa từ khóa (VD: 'họ tên', 'điện thoại', 'email', 'địa chỉ', 'tỉnh').
        Cấu trúc thực tế: <div data-slot="error-message" class="text-tiny text-danger">...</div>
        """
        try:
            xpath = (
                "//div[@data-slot='error-message' and "
                f"contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{keyword.lower()}')]"
            )
            el = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            return el.text.strip()
        except TimeoutException:
            return ""

    # ====== HÀM LẤY LỖI CHI TIẾT CHO TỪNG FIELD ======
    def get_name_error(self):
        return self._get_error_by_text("họ tên")

    def get_phone_error(self):
        """
        Bắt lỗi 'Vui lòng nhập số điện thoại' (locator động của React).
        Ưu tiên lấy qua div[@data-slot='error-message'], fallback bằng HTML5 validation.
        """
        try:
            msg = self._get_error_by_text("số điện thoại") or self._get_error_by_text("điện thoại")
            if msg:
                return msg
            # fallback HTML5 validation (rare case)
            phone_input = self.driver.find_element(*self.PHONE)
            validation = phone_input.get_attribute("validationMessage")
            if validation:
                return validation
        except Exception:
            pass
        return ""

    def get_email_error(self):
        return self._get_error_by_text("email")

    def get_address_error(self):
        return self._get_error_by_text("địa chỉ")

    def get_province_error(self):
        """Lỗi thiếu tỉnh/thành phố."""
        return self._get_error_by_text("tỉnh") or self._get_error_by_text("thành phố")
