from datetime import datetime
import pytest
from Page.order_page import OrderPage
from Utils.data_reader import read_csv_data
from Utils.test_result_writer_excel import write_test_results_excel

BASE_URL = "https://swe.vn/"
all_results = []  # Lưu toàn bộ kết quả test để ghi 1 lần sau cùng


@pytest.mark.parametrize("keyword,quantity", read_csv_data("Data/data_order.csv"))
def test_order_flow(driver, keyword, quantity):
    """
    Kiểm thử luồng đặt hàng cơ bản:
    - Tìm sản phẩm
    - Chọn sản phẩm đầu tiên
    - Tăng số lượng
    - Thêm vào giỏ hàng
    - Mở giỏ hàng
    - Kiểm tra thông báo
    """
    test_name = f"Order_{keyword}_{quantity}"
    page = OrderPage(driver)
    page.open(BASE_URL)

    try:
        # Thực hiện các bước
        page.search_product(keyword)
        page.click_first_result()
        page.increase_quantity(quantity)
        page.add_to_cart()
        page.view_cart()
        message = page.get_cart_message()

        # Kiểm tra kết quả
        if any(word in message.lower() for word in ["giỏ hàng", "cart", "success", "thành công"]):
            status = "PASS"
        else:
            status = "FAIL"

        actual = message

    except Exception as e:
        status = "FAIL"
        actual = str(e)

    # Ghi lại kết quả tạm thời
    all_results.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Test Name": test_name,
        "Keyword": keyword,
        "Quantity": quantity,
        "Actual": actual,
        "Status": status
    })

    # Assertion cuối cùng để pytest đánh dấu pass/fail
    assert status == "PASS", f"[{test_name}] Expected: Success - Actual: {actual}"


def teardown_module(module):
    """Sau khi chạy xong module, ghi toàn bộ kết quả ra file Excel"""
    if all_results:
        write_test_results_excel(
            all_results,
            filename="Reports/test_results_order.xlsx",
            sheet_name="Order Test Results"
        )
