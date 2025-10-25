import csv
import json
import openpyxl
import os

def get_data(file_path, file_type="csv"):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f" Không tìm thấy file dữ liệu: {file_path}")

    file_type = file_type.lower()

    # ---- CSV ----
    if file_type == "csv":
        with open(file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader]
            return _normalize_data(rows)

    # ---- JSON ----
    elif file_type == "json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Đảm bảo luôn trả về list
            if isinstance(data, dict):
                data = [data]
            return _normalize_data(data)

    # ---- EXCEL ----
    elif file_type in ["excel", "xlsx"]:
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active
        headers = [cell.value for cell in sheet[1]]
        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if any(row):
                data.append(dict(zip(headers, row)))
        return _normalize_data(data)

    else:
        raise ValueError(f" Không hỗ trợ định dạng file: {file_type}")


def _normalize_data(data):
    if not data:
        return []

    first = data[0]

    # Nếu là test thêm giỏ hàng → tuple
    if all(k in first for k in ["keyword", "quantity"]):
        return [(item["keyword"], item["quantity"]) for item in data]

    # Các loại test khác → dict
    return data
