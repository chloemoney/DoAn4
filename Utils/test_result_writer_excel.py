# Utils/test_result_writer_excel.py
import os
import csv

# cố gắng import openpyxl; nếu không có sẽ dùng fallback CSV
try:
    from openpyxl import Workbook
    from openpyxl.utils import get_column_letter
    _HAS_OPENPYXL = True
except Exception:
    _HAS_OPENPYXL = False

def write_test_results_excel(results, filename="reports/test_results_order.xlsx", sheet_name="Test Results"):
    if results is None:
        results = []

    # đảm bảo thư mục tồn tại (nếu có)
    dirpath = os.path.dirname(filename)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    headers = ["Time", "Test Name", "Keyword", "Quantity", "Actual", "Status"]

    # Nếu openpyxl có sẵn và filename là .xlsx -> ghi Excel
    if _HAS_OPENPYXL and filename.lower().endswith((".xlsx", ".xlsm", ".xltx", ".xltm")):
        wb = Workbook()
        ws = wb.active
        ws.title = sheet_name

        # header
        ws.append(headers)

        # rows
        for r in results:
            ws.append([r.get(h, "") for h in headers])

        # auto width
        for i, column_cells in enumerate(ws.columns, 1):
            try:
                max_length = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
            except Exception:
                max_length = 0
            ws.column_dimensions[get_column_letter(i)].width = max_length + 2

        wb.save(filename)
        print(f"Test results saved to {os.path.abspath(filename)}")
        return os.path.abspath(filename)

    # fallback: ghi CSV (nếu filename là .xlsx thì đổi thành .csv)
    csv_path = filename
    if filename.lower().endswith(".xlsx"):
        csv_path = filename[:-5] + ".csv"

    with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for r in results:
            writer.writerow([r.get(h, "") for h in headers])

    if _HAS_OPENPYXL:
        print(f"Lưu ra CSV tại {os.path.abspath(csv_path)} (openpyxl đã cài nhưng filename không .xlsx)")
    else:
        print(f"openpyxl không cài — đã ghi CSV thay thế tại {os.path.abspath(csv_path)}")
    return os.path.abspath(csv_path)
