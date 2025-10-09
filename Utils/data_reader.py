import os
import csv

def read_csv_data(file_name):
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_dir, file_name)
    with open(file_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        return list(reader)

def get_data(file_path):
    data = []
    abs_path = os.path.join(os.getcwd(), file_path)

    with open(abs_path, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cleaned_row = {k.strip(): v.strip() for k, v in row.items()}
            data.append((cleaned_row["keyword"], cleaned_row["quantity"]))
            data.append(next(iter(row.values())))
    return data
def get_data(file_path):
    data = []
    abs_path = os.path.join(os.getcwd(), file_path)

    with open(abs_path, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cleaned_row = {k.strip(): v.strip() for k, v in row.items()}
            data.append((cleaned_row["keyword"]))
            data.append(next(iter(row.values())))
    return data

