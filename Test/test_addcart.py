# Test/test_addcart.py
import os
import time
import pytest
from Page.addcart_page import AddCartPage
from Utils.data_reader import get_data
from Utils.test_result_writer_excel import log_result

BASE_URL = "https://swe.vn/"

DATA_FILE = "Data/data_addcart.json"
DATA_TYPE = "json"


# Pytest sẽ tự động tạo test cho từng dòng dữ liệu
@pytest.mark.parametrize("keyword,quantity", get_data(DATA_FILE, DATA_TYPE))
def test_add_to_cart(driver, keyword, quantity):
    page = AddCartPage(driver)
    try:
        print(f"\n Đang test sản phẩm: '{keyword}' với số lượng {quantity}")

        page.open(BASE_URL)
        page.search_product(keyword)
        page.open_first_product()

        # Click nút '+' đúng (quantity - 1) lần: mỗi click +1 sản phẩm
        page.increase_quantity(quantity)
        print(f" Đã click dấu '+' {int(quantity) - 1} lần.")

        page.add_to_cart()

        message = page.get_toast_message()
        assert any(w in message.lower() for w in ["giỏ hàng", "thành công", "added", "success"]), \
            f"Không thấy thông báo thêm vào giỏ hàng. Nhận được: {message}"

        page.view_cart()
        time.sleep(2)
        cart_qty = page.get_cart_quantity()
        assert cart_qty == int(quantity), \
            f"Số lượng trong giỏ hàng ({cart_qty}) không khớp với ({quantity})"

        log_result(keyword, quantity, "PASS", "Thêm sản phẩm vào giỏ hàng thành công")

    except AssertionError as e:
        handle_exception(driver, keyword, quantity, "FAIL", str(e))
        raise
    except Exception as e:
        handle_exception(driver, keyword, quantity, "ERROR", str(e))
        raise


def handle_exception(driver, keyword, quantity, status, message):
    os.makedirs("report/screenshots", exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    safe_keyword = str(keyword).replace(" ", "_").replace("/", "_")
    screenshot_path = f"report/screenshots/{safe_keyword}_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
    log_result(keyword, quantity, status, message, screenshot_path)
