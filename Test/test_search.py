
import os
import csv
from datetime import datetime
import re
import pytest
from Page.search_page import SearchPage
from Utils.data_reader import read_csv_data


def load_csv(path=None):
    if path is None:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        path = os.path.join(project_root, "Data", "data_search.csv")  # <--- chỉnh tên file nếu khác
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy file data: {path}")
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "search": r.get("search", "") if r.get("search", "") is not None else "",
                "expected": r.get("expected", "") if r.get("expected", "") is not None else ""
            })
    return rows

test_data = read_csv_data("Data/data_search.csv")
all_results = []

# --- helper so sánh nhỏ gọn và robust ---
def _norm(s: str) -> str:
    if s is None:
        return ""
    s = str(s)
    s = s.replace("“", '"').replace("”", '"').replace("’", "'")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s

def _match(expected: str, actual: str) -> bool:
    e = _norm(expected)
    a = _norm(actual)
    if not e and not a:
        return True
    if not a:
        return False
    return (e in a) or (a in e)

# --- tests ---
@pytest.mark.parametrize("row", test_data)
def test_search(driver, row):
    page = SearchPage(driver)

    keyword = row["search"]           # giữ nguyên (không strip) — để test các trường hợp leading spaces
    expected = row["expected"]

    test_name = f"test_search_{repr(keyword)}"
    actual = ""
    status = "FAIL"

    # mở trang và tìm
    page.open("https://swe.vn/")
    page.search(keyword)

    try:
        actual = page.get_search_message() or ""
        if _match(expected, actual):
            status = "PASS"
        else:
            status = "FAIL"
    except Exception as ex:
        actual = f"EXCEPTION: {ex}"
        status = "FAIL"

    # lưu kết quả (ghi sau cùng trong teardown_module)
    all_results.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Test Name": test_name,
        "Keyword": keyword,
        "Expected": expected,
        "Actual": actual,
        "Status": status
    })

    assert status == "PASS", f"[{test_name}] Expected: {expected}\nActual: {actual}"


def teardown_module(module):
    from Utils.test_result_writer_excel import write_test_results_excel
    write_test_results_excel(
        all_results,
        filename="test_results_search.xlsx",
        sheet_name="Test Results Search"
    )