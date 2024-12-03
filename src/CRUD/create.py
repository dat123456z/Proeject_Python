import tkinter as tk
from tkinter import messagebox
#from CRUD.update import check_car_exists
import csv
import re
from datetime import datetime

def save_data_to_csv(columns, car_data):
    file_path = 'data/clean/Cleaned_Car_Dataset.csv'
    try:
        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)
            writer.writerows(car_data)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")



def validate_input(car_data, entries):
    """Kiểm tra dữ liệu nhập vào có hợp lệ không."""
    # Kiểm tra Car_id (Số nguyên)
    car_id = entries["Car_id"].get()
    if not car_id.isdigit():
        messagebox.showerror("Error", "Car ID must be a number.")
        entries["Car_id"].delete(0, tk.END)
        entries["Car_id"].focus_set()
        return False
    #if check_car_exists(car_id, car_data):
    #    messagebox.showerror("Error", "Car ID already exists. Please enter another ID.")
    #    entries["Car_id"].delete(0, tk.END)
    #    entries["Car_id"].focus_set()
    #    return False

    # Kiểm tra Date (Ngày hợp lệ)
    date = entries["Date"].get()
    try:
        datetime.strptime(date, "%m/%d/%Y")  # Định dạng ngày: YYYY-MM-DD
    except ValueError:
        messagebox.showerror("Error", "Date must be in the format MM/DD/YYYY.")
        entries["Date"].delete(0, tk.END)
        entries["Date"].focus_set()
        return False

    # Kiểm tra Customer Name (Chuỗi)
    customer_name = entries["Customer Name"].get()
    if not all(c.isalpha() or c.isspace() for c in customer_name):
        messagebox.showerror("Error", "Customer Name must be a valid string.")
        entries["Customer Name"].delete(0, tk.END)
        entries["Customer Name"].focus_set()
        return False

    # Kiểm tra Gender (Male hoặc Female)
    gender = entries["Gender"].get().lower()
    if gender not in ['male', 'female']:
        messagebox.showerror("Error", "Gender must be either 'Male' or 'Female'.")
        entries["Gender"].delete(0, tk.END)
        entries["Gender"].focus_set()
        return False

    # Kiểm tra Annual Income (Số nguyên)
    try:
        annual_income = int(entries["Annual Income"].get())
        if annual_income <= 0:
            messagebox.showerror("Error", "Annual Income must be a positive integer.")
            entries["Annual Income"].delete(0, tk.END)
            entries["Annual Income"].focus_set()
            return False
    except ValueError:
        messagebox.showerror("Error", "Annual Income must be a valid integer.")
        entries["Annual Income"].delete(0, tk.END)
        entries["Annual Income"].focus_set()
        return False

    # Kiểm tra Dealer Name (Chuỗi)
    #dealer_name = entries["Dealer_Name"].get()
    #if not dealer_name.isalpha() and not re.match("^[A-Za-z\s]+$", dealer_name):
    #    messagebox.showerror("Error", "Dealer Name must be a valid string.")
    #    entries["Dealer_Name"].delete(0, tk.END)
    #    entries["Dealer_Name"].focus_set()
    #    return False

    # Kiểm tra Dealer_Name, Company, Color (Chuỗi)
    for field in ["Dealer_Name", "Company", "Color"]:
        value = entries[field].get()
        if not all(c.isalpha() or c.isspace() for c in value):
            messagebox.showerror("Error", f"{field} must be a valid string.")
            entries[field].delete(0, tk.END)
            entries[field].focus_set()
            return False

    # Kiểm tra Price (Số nguyên)
    try:
        price = int(entries["Price"].get())
        if price <= 0:
            messagebox.showerror("Error", "Price must be a positive integer.")
            entries["Price"].delete(0, tk.END)
            entries["Price"].focus_set()
            return False
    except ValueError:
        messagebox.showerror("Error", "Price must be a valid integer.")
        entries["Price"].delete(0, tk.END)
        entries["Price"].focus_set()
        return False

    # Kiểm tra Phone (Số nguyên)
    phone = entries["Phone"].get()
    if not phone.isdigit():
        messagebox.showerror("Error", "Phone must be a valid number.")
        entries["Phone"].delete(0, tk.END)
        entries["Phone"].focus_set()
        return False

    return True


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
        messagebox.showwarning("Error", "Please fill in the data completely")  # Hiển thị thông báo
        first_empty_field = empty_fields[0]  # Trường trống đầu tiên
        entries[first_empty_field].focus_set()  # Đặt con trỏ vào trường trống đầu tiên
        return  # Giữ nguyên input_frame để người dùng có thể nhập tiếp

     # Kiểm tra tính hợp lệ của dữ liệu nhập vào
    if not validate_input(car_data, entries):
        return  # Dừng lại nếu dữ liệu không hợp lệ

    car_data.append(new_car)  # Lưu xe mới vào danh sách dữ liệu
    tree.insert("", tk.END, values=new_car)  # Hiển thị dữ liệu trên bảng
    save_data_to_csv(columns, car_data)  # Lưu vào file CSV, truyền columns và car_data

    # Hiển thị thông báo thành công
    messagebox.showinfo("", "Add car successfully")

    # Xóa dữ liệu trong các entry sau khi thêm thành công
    for entry in entries.values():
        entry.delete(0, tk.END)

    input_frame.pack_forget()  # Ẩn khung nhập liệu
    table_frame.pack(fill="both", expand=True)  # Hiển thị lại bảng dữ liệu
