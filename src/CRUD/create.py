import tkinter as tk
from tkinter import messagebox
import csv

def save_data_to_csv(columns, car_data):
    file_path = 'data/clean/Cleaned_Car_Dataset.csv'
    try:
        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)
            writer.writerows(car_data)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

def add_car(columns, entries, car_data, tree, input_frame, table_frame):
    new_car = []
    empty_fields = []  # Danh sách để lưu trữ các trường trống

    for col in columns:
        value = entries[col].get()
        if not value:
            empty_fields.append(col)  # Thêm tên cột vào danh sách nếu còn trống
        new_car.append(value)

    # Kiểm tra nếu có trường trống
    if empty_fields:
        messagebox.showwarning("Lỗi nhập liệu", "Vui lòng điền vào đầy đủ dữ liệu.")  # Hiển thị thông báo
        first_empty_field = empty_fields[0]  # Trường trống đầu tiên
        entries[first_empty_field].focus_set()  # Đặt con trỏ vào trường trống đầu tiên
        return  # Giữ nguyên input_frame để người dùng có thể nhập tiếp

    car_data.append(new_car)  # Lưu xe mới vào danh sách dữ liệu
    tree.insert("", tk.END, values=new_car)  # Hiển thị dữ liệu trên bảng
    save_data_to_csv(columns, car_data)  # Lưu vào file CSV, truyền columns và car_data

    # Hiển thị thông báo thành công
    messagebox.showinfo("", "Thêm xe thành công.")

    # Xóa dữ liệu trong các entry sau khi thêm thành công
    for entry in entries.values():
        entry.delete(0, tk.END)

    input_frame.pack_forget()  # Ẩn khung nhập liệu
    table_frame.pack(fill="both", expand=True)  # Hiển thị lại bảng dữ liệu
