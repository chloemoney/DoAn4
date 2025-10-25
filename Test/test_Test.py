import pytest
from selenium import webdriver
from Page.test_page import AddToCartPage
from Utils.data_reader import get_data_from_csv


@pytest.fixture()
def setup():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.mark.parametrize("keyword", get_data_from_csv("Data/data_test.csv"))
def test_add_to_cart_flow(setup, keyword):
    driver = setup
    page = AddToCartPage(driver)

    # 1️⃣ Mở trang chủ
    page.open_homepage()

    # 2️⃣ Tìm kiếm sản phẩm
    page.search_product(keyword)

    # 3️⃣ Nhấn vào sản phẩm đầu tiên
    page.open_first_product()

    # 4️⃣ Bấm "Thêm vào giỏ hàng"
    page.add_to_cart()

    # 5️⃣ Bấm "Xem giỏ hàng"
    page.view_cart()

    # 6️⃣ Kiểm tra đã vào trang giỏ hàng
    assert page.is_cart_page_displayed(), f" Không vào được trang giỏ hàng sau khi thêm {keyword}"

    print(f" Thêm sản phẩm '{keyword}' vào giỏ hàng thành công!")
