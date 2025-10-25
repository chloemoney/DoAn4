import time
import pytest
from datetime import datetime
from Page.order_page import CheckoutPage
from Utils.data_reader import get_data   # ✅ thay vì read_csv
from Utils.test_result_writer_excel import ExcelReporter


DATA_FILE = "Data/data_order.json"    # ← đổi sang .csv hoặc .xlsx khi cần
DATA_TYPE = "json"                    # ← đổi tương ứng: csv / json / excel

# Đọc dữ liệu theo loại file
test_data = get_data(DATA_FILE, DATA_TYPE)


class TestCheckout:

    @pytest.mark.parametrize("data", test_data)
    def test_checkout_field_errors(self, driver, data):
        page = CheckoutPage(driver)
        reporter = ExcelReporter("report/test_results_order.xlsx")

        keyword = data.get("keyword", "")
        name = data.get("name", "")
        phone = data.get("phone", "")
        email = data.get("email", "")
        province = data.get("province", "")
        address = data.get("address", "")
        expected = str(data.get("expected", "")).strip().lower()
        test_name = f"checkout_{expected}_{keyword[:12]}"

        actual_error = ""
        status = "FAIL"

        try:
            # --- FLOW TEST ---
            driver.get("https://swe.vn/")
            page.search_product(keyword)
            page.click_first_product()
            page.add_to_cart()
            page.go_to_checkout_from_popup()
            page.fill_checkout_form(name, phone, email, province, address)
            page.submit_order()

            # --- KIỂM TRA LỖI HIỂN THỊ ---
            if expected == "name":
                actual_error = page.get_name_error()
            elif expected == "phone":
                actual_error = page.get_phone_error()
            elif expected == "email":
                actual_error = page.get_email_error()
            elif expected == "address":
                actual_error = page.get_address_error()
            elif expected == "province":
                actual_error = page.get_province_error()

            if actual_error:
                status = "PASS"
            else:
                raise AssertionError("Không thấy lỗi hiển thị đúng vị trí!")

        except Exception as e:
            actual_error = str(e)

        finally:
            reporter.write_result({
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Test Name": test_name,
                "Keyword": keyword,
                "Name": name,
                "Phone": phone,
                "Email": email,
                "Province": province,
                "Address": address,
                "Expected": expected,
                "Actual Error": actual_error,
                "Status": status
            })

        assert status == "PASS", f"[{test_name}] Expected '{expected}', got: {actual_error}"
