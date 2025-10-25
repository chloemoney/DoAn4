import pytest
import time
import os
from datetime import datetime
from Page.addcart2_page import CartPage
from Utils.test_result_writer_excel import ExcelReporter  # dùng class bạn đã có


@pytest.mark.usefixtures("driver")
class TestCartSingle:

    def test_add_reduce_remove_cart(self, driver):
        keyword = "SWE PIPELINE JEANS - RETRO BLUE"
        page = CartPage(driver)
        reporter = ExcelReporter("report/test_results_cart.xlsx")

        status = "FAIL"
        error_msg = ""
        screenshot_path = ""

        try:
            page.open_homepage()

            page.search_product(keyword)

            page.open_first_product()

            page.increase_quantity(3)

            page.add_to_cart()

            page.view_cart()

            page.decrease_quantity(1)
            qty = page.get_cart_quantity()
            assert qty == 3, f"Số lượng mong đợi 3, thực tế {qty}"

            page.remove_product()

            assert page.is_cart_empty(), "Giỏ hàng chưa trống sau khi xóa sản phẩm!"

            status = "PASS"
            print(" Testcase hoàn tất: Thêm – Giảm – Xóa sản phẩm thành công!")

        except AssertionError as e:
            error_msg = str(e)
            screenshot_path = self.capture_screenshot(driver, "assert_fail")
            print(f" AssertionError: {error_msg}")

        except Exception as e:
            error_msg = str(e)
            screenshot_path = self.capture_screenshot(driver, "exception")
            print(f" Lỗi không mong đợi: {error_msg}")

        finally:
            reporter.write_result({
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Test Name": "Thêm – Giảm – Xóa sản phẩm",
                "Keyword": keyword,
                "Expected": "Giỏ hàng trống sau khi xóa",
                "Actual": error_msg if error_msg else "Hoàn thành đúng",
                "Status": status,
                "Screenshot": screenshot_path
            })

            assert status == "PASS", f"Test không đạt: {error_msg}"

    # ========== HÀM CHỤP ẢNH ==========
    def capture_screenshot(self, driver, prefix="screenshot"):
        os.makedirs("report/screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = f"report/screenshots/{prefix}_{timestamp}.png"
        driver.save_screenshot(path)
        return path
