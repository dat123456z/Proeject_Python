import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from showchart import show_chart

# Data storage
car_data = []
columns = ["Car_id", "Date", "Customer Name", "Gender", "Annual Income", "Dealer_Name", "Company", "Model", "Color", "Price", "Phone"]

# Hàm mở cửa sổ nhập dữ liệu
def open_input_window():
    table_frame.pack_forget()
    input_frame.pack(fill="x", pady=20)

    for widget in input_frame.winfo_children():
        widget.destroy()

    global entries
    entries = {}
    for idx, col in enumerate(columns):
        label = tk.Label(input_frame, text=col, font=('Helvetica', 10, 'bold'), fg="#333333", bg="#d9f2e6")
        label.grid(row=idx, column=0, sticky='w', padx=10, pady=8)

        entry = ttk.Entry(input_frame, width=50)
        entry.grid(row=idx, column=1, padx=10, pady=8)

         # Kiểm tra ngay khi nhập Car ID
        if col == "Car_id":
            entry.bind("<KeyRelease>", check_id_on_entry)  # Gọi hàm kiểm tra mỗi khi có thay đổi
            global id_warning_label
            id_warning_label = tk.Label(input_frame, text="", font=('Helvetica', 9), fg="red", bg="#d9f2e6")
            id_warning_label.grid(row=idx, column=2, padx=10, pady=8)
        
        entries[col] = entry

    save_button = tk.Button(input_frame, text="Save", command=save_and_view_data, bg="#007bff", fg="white", font=('Helvetica', 10, 'bold'), bd=0, padx=20, pady=5)
    save_button.grid(row=len(columns), column=0, columnspan=2, pady=10)

def check_id_on_entry(event):
    car_id = entries["Car_id"].get()
    if check_car_exists(car_id):
        id_warning_label.config(text="ID đã tồn tại.", fg="green")  # Hiển thị cảnh báo nếu ID tồn tại
    else:
        id_warning_label.config(text="")  # Ẩn cảnh báo nếu ID chưa tồn tại

def check_car_exists(car_id):
    for car in car_data:
        if car[0] == car_id:
            return True
    return False

def save_and_view_data():
    car_id = entries["Car_id"].get()
    if check_car_exists(car_id):
        messagebox.showerror("Lỗi", "ID xe đã tồn tại. Vui lòng nhập ID khác")
        entries["Car_id"].delete(0, tk.END)
        entries["Car_id"].focus_set()  # Đặt con trỏ vào Car ID để nhập lại
    else:
        if add_car():  # Gọi add_car và chỉ ẩn input_frame nếu thêm thành công
            input_frame.pack_forget()
            table_frame.pack(fill="both", expand=True)
            view_data()

def update_car(car_id):
    for car in car_data:
        if car[0] == car_id:
            open_input_window_for_update(car_id)
            return
    messagebox.showerror("Error", "Car ID not found.")


# Sửa hàm load_data_from_csv để ẩn input_frame và hiển thị lại table_frame
def load_data_from_csv():
    input_frame.pack_forget()  # Ẩn khung nhập liệu
    table_frame.pack(fill="both", expand=True)  # Hiển thị lại khung bảng dữ liệu

    file_path = 'data.csv'
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            car_data.clear()
            for row in reader:
                car_data.append(row)
        view_data()
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{file_path}' not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")

def view_data():
    for row in tree.get_children():
        tree.delete(row)
    for row in car_data:
        tree.insert("", tk.END, values=row)

def add_car():
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
    save_data_to_csv()  # Lưu vào file CSV

    # Hiển thị thông báo thành công
    messagebox.showinfo("", "Thêm xe thành công.")

    # Xóa dữ liệu trong các entry sau khi thêm thành công
    for entry in entries.values():
        entry.delete(0, tk.END)

    input_frame.pack_forget()  # Ẩn khung nhập liệu
    table_frame.pack(fill="both", expand=True)  # Hiển thị lại bảng dữ liệu


def save_data_to_csv():
    file_path = 'data.csv'
    try:
        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)
            writer.writerows(car_data)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

def update_car_by_id():
    update_window = tk.Toplevel(root)
    update_window.title("Cập nhật xe")
    update_window.geometry("300x150")

    # Tính toán để cửa sổ update_window hiển thị ở giữa root
    x = root.winfo_x() + (root.winfo_width() // 2) - (300 // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (150 // 2)
    update_window.geometry(f"300x150+{x}+{y}")

    tk.Label(update_window, text="Nhập ID xe muốn cập nhật:", font=('Helvetica', 10)).pack(pady=10)
    car_id_entry = ttk.Entry(update_window, width=30)
    car_id_entry.pack(pady=5)

    def check_and_update():
        car_id = car_id_entry.get()
        if not car_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID.")
            return

        # Kiểm tra xem ID có tồn tại không
        if not any(car[0] == car_id for car in car_data):  # Nếu ID không tồn tại trong dữ liệu
            # Tạo cửa sổ thông báo lỗi và định vị ở giữa root
            error_window = tk.Toplevel(update_window)
            error_window.title("Lỗi")
            error_window.geometry("300x100")
            
            # Tính toán để cửa sổ error_window hiển thị ở giữa root
            err_x = root.winfo_x() + (root.winfo_width() // 2) - (300 // 2)
            err_y = root.winfo_y() + (root.winfo_height() // 2) - (100 // 2)
            error_window.geometry(f"300x100+{err_x}+{err_y}")
            
            tk.Label(error_window, text="ID không tồn tại.", font=('Helvetica', 10)).pack(pady=10)
            
            # Nút "Nhập lại" để người dùng có thể nhập lại ID
            retry_button = ttk.Button(error_window, text="Nhập lại", command=lambda: [car_id_entry.delete(0, tk.END), error_window.destroy()])
            retry_button.pack(side=tk.LEFT, padx=10, pady=10)

            # Nút "Hủy" để đóng cả hai cửa sổ
            cancel_button = ttk.Button(error_window, text="Hủy", command=lambda: [error_window.destroy(), update_window.destroy()])
            cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)
            return

        # Nếu ID tồn tại, thực hiện mở cửa sổ cập nhật và đóng cửa sổ hiện tại
        update_window.destroy()
        open_input_window_for_update(car_id)

    ttk.Button(update_window, text="Cập nhật", command=check_and_update).pack(pady=10)



def open_input_window_for_update(car_id):
    table_frame.pack_forget()
    input_frame.pack(fill="x", pady=20)

    for widget in input_frame.winfo_children():
        widget.destroy()

    global entries
    entries = {}
    for idx, col in enumerate(columns):
        label = tk.Label(input_frame, text=col, font=('Helvetica', 10, 'bold'), fg="#333333", bg="#d9f2e6")
        label.grid(row=idx, column=0, sticky='w', padx=10, pady=8)
        entry = ttk.Entry(input_frame, width=50)
        entry.grid(row=idx, column=1, padx=10, pady=8)
        
        for car in car_data:
            if car[0] == car_id:
                entry.insert(0, car[idx])
                break
        entries[col] = entry

    save_button = tk.Button(input_frame, text="Save", command=lambda: save_updated_car(car_id), bg="#007bff", fg="white", font=('Helvetica', 10, 'bold'), bd=0, padx=20, pady=5)
    save_button.grid(row=len(columns), column=0, columnspan=2, pady=10)

def save_updated_car(car_id):
    updated_car = []
    for col in columns:
        value = entries[col].get()
        if not value:
            messagebox.showwarning("Lỗi nhập liệu", "Vui lòng điền vào đầy đủ dữ liệu.")
            return
        updated_car.append(value)
    
    for i, car in enumerate(car_data):
        if car[0] == car_id:
            car_data[i] = updated_car
            break

    save_data_to_csv()
    input_frame.pack_forget()
    table_frame.pack(fill="both", expand=True)
    view_data()
    messagebox.showinfo("", "Cập nhật dữ liệu thành công.")

def delete_car():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No selection", "Please select a row to delete.")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected row?")
    if confirm:
        data_index = tree.index(selected_item[0])
        del car_data[data_index]
        save_data_to_csv()
        view_data()

def quit_app():
    root.quit()

# Giao diện chính
root = tk.Tk()
root.title("Car Management System")
root.geometry("1500x700")
root.configure(bg="#e6f7ff")

# Sidebar với màu nền xanh nhạt
sidebar = tk.Frame(root, bg="#d9f2e6", width=100, height=700)
sidebar.pack(side="left", fill="y")

# Logo
def create_logo():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, "logo.png")
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((80, 80), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(sidebar, image=logo_photo, bg="#d9f2e6")
        logo_label.image = logo_photo
        logo_label.grid(row=0, column=0, padx=10, pady=10)
    except FileNotFoundError:
        messagebox.showerror("Error", "Logo file 'logo.png' not found.")
create_logo()

def create_nav_button(text, row, command=None):
    btn = tk.Button(sidebar, text=text, font=("Helvetica", 10, "bold"), fg="white", bg="#007bff", bd=0, padx=10, pady=10, command=command)
    btn.grid(row=row, column=0, sticky="ew", padx=10, pady=10)

create_nav_button("📂 Load Data", 1, load_data_from_csv)
create_nav_button("➕ Add Car", 2, open_input_window)
create_nav_button("🖉 Update Car", 3, update_car_by_id)
create_nav_button("🗑 Delete Car", 4, delete_car)
create_nav_button("📊 Show Chart", 5, show_chart)
create_nav_button("🚪 Quit", 6, quit_app)

main_frame = tk.Frame(root, bg="#e6f7ff", padx=20, pady=20)
main_frame.pack(side="right", fill="both", expand=True)

title_label = tk.Label(main_frame, text="CAR MANAGEMENT APP", font=("Helvetica", 24, 'bold'), bg="#e6f7ff", fg="green")
title_label.pack()

input_frame = tk.Frame(main_frame, bg="#d9f2e6", padx=20, pady=20, bd=2, relief="groove")
input_frame.pack_forget()

table_frame = tk.Frame(main_frame, bg="#d9f2e6", bd=2, relief="groove")
table_frame.pack(fill="both", expand=True)

tree = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

load_data_from_csv()
view_data()

# Bắt đầu vòng lặp sự kiện Tkinter
root.mainloop()

