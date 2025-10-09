import pytest
from Page.product_page import AddCartPage
from Utils.data_reader import get_data

BASE_URL = "https://swe.vn/"

@pytest.mark.parametrize("keyword", get_data("Data/data_addcart.csv"))
def test_add_to_cart(driver, keyword):
    page = AddCartPage(driver)

    page.open(BASE_URL)
    page.search_product(keyword)
    page.open_first_product()
    page.add_to_cart()

    message = page.get_toast_message()

    assert any(word in message.lower() for word in ["giỏ hàng", "thành công", "added", "success"]), \
        f" Không thấy thông báo thêm vào giỏ hàng. Nhận được: {message}"
