import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        # Link mở popup login
        self.login_link = (By.CSS_SELECTOR, "a[id='site-account-handle'] span[class='icon-box-text']")
        # Trường email (theo name)
        self.email_field = (By.CSS_SELECTOR, "input[name='customer[email]']")
        # Trường password
        self.password_field = (By.CSS_SELECTOR, "input[name='customer[password]']")
        # Nút đăng nhập
        self.login_button = (By.CSS_SELECTOR, "#form_submit-login")

    def open(self, url):
        self.driver.get(url)

    def login(self, email, password):
        # Click mở form login
        self.driver.find_element(*self.login_link).click()

        email_input = self.driver.find_element(*self.email_field)
        password_input = self.driver.find_element(*self.password_field)


        email_input.clear()
        password_input.clear()

        if email:
            email_input.send_keys(email)
        if password:
            password_input.send_keys(password)


        time.sleep(2)
        self.driver.find_element(*self.login_button).click()
        time.sleep(2)

    def get_error_message(self):

        try:
            email_input = self.driver.find_element(*self.email_field)
            password_input = self.driver.find_element(*self.password_field)

            if email_input.get_attribute("validationMessage"):
                return email_input.get_attribute("validationMessage")

            if password_input.get_attribute("validationMessage"):
                return password_input.get_attribute("validationMessage")

            # Có thể có alert/message khác (tùy HTML của swe.vn sau khi login fail)
            return ""
        except NoSuchElementException:
            return ""
