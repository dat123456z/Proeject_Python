import tkinter as tk
from src.CRUD.create import save_data_to_csv, add_car

# Hàm sắp xếp cột
def sort_column(col, columns, sort_states, car_data, tree):
    """Sắp xếp dữ liệu dựa trên cột được bấm vào trong Treeview"""
    reverse = sort_states[col]
    try:
        sorted_data = sorted(car_data, key=lambda x: float(x[columns.index(col)]), reverse=reverse)
    except ValueError:
        sorted_data = sorted(car_data, key=lambda x: x[columns.index(col)], reverse=reverse)
    sort_states[col] = not reverse
    view_data(sorted_data, tree= tree, car_data=car_data)  # Truyền dữ liệu đã sắp xếp


# Hàm hiển thị dữ liệu lên bảng
def view_data(data=None, tree=None, car_data=None):
    for row in tree.get_children():
        tree.delete(row)
    data_to_display = data if data else car_data
    for row in data_to_display:
        tree.insert("", tk.END, values=row)