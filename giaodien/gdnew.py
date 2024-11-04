import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image, ImageTk

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
        entries[col] = entry

    save_button = tk.Button(input_frame, text="Save", command=save_and_view_data, bg="#007bff", fg="white", font=('Helvetica', 10, 'bold'), bd=0, padx=20, pady=5)
    save_button.grid(row=len(columns), column=0, columnspan=2, pady=10)

def save_and_view_data():
    car_id = entries["Car_id"].get()
    if check_car_exists(car_id):
                update_car(car_id)
        
def update_car(car_id):
    for car in car_data:
        if car[0] == car_id:
            open_input_window_for_update(car_id)
            return
        messagebox.showerror("Error", "Car ID not found.")
    else:
        add_car()
    input_frame.pack_forget()
    table_frame.pack(fill="both", expand=True)
    view_data()

def check_car_exists(car_id):
    for car in car_data:
        if car[0] == car_id:
            return True
    return False

def load_data_from_csv():
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
    for col in columns:
        value = entries[col].get()
        if not value:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        new_car.append(value)
    car_data.append(new_car)
    tree.insert("", tk.END, values=new_car)
    save_data_to_csv()
    for entry in entries.values():
        entry.delete(0, tk.END)

def save_data_to_csv():
    file_path = 'data.csv'
    try:
        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)
            writer.writerows(car_data)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

# Hàm mở cửa sổ nhập car_id cần cập nhật
def update_car_by_id():
    update_window = tk.Toplevel(root)
    update_window.title("Update Car")
    update_window.geometry("300x150")
    
    tk.Label(update_window, text="Enter the car id you want to update:", font=('Helvetica', 10)).pack(pady=10)
    car_id_entry = ttk.Entry(update_window, width=30)
    car_id_entry.pack(pady=5)

    def check_and_update():
        car_id = car_id_entry.get()
        if not car_id:
            messagebox.showwarning("Warning", "Please enter a car ID.")
            return

        for car in car_data:
            if car[0] == car_id:
                update_window.destroy()
                open_input_window_for_update(car_id)
                return

        messagebox.showerror("Error", "Không có ID vừa nhập")
        tk.Button(update_window, text="Nhập lại ID", command=lambda: car_id_entry.delete(0, tk.END)).pack(pady=5)
        tk.Button(update_window, text="Cancel", command=update_window.destroy).pack(pady=5)

    ttk.Button(update_window, text="OK", command=check_and_update).pack(pady=10)

# Hàm mở cửa sổ nhập dữ liệu để cập nhật thông tin của xe
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
            messagebox.showwarning("Input Error", "Please fill in all fields.")
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
    messagebox.showinfo("Success", "Car data updated successfully.")

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

def show_chart():
    if not car_data:
        messagebox.showwarning("No Data", "Please load data first.")
        return

    df = pd.DataFrame(car_data, columns=columns)
    company_counts = df['Company'].value_counts()
    total_count = company_counts.sum()
    top_5_companies = company_counts.nlargest(5)
    top_5_percentages = (top_5_companies / total_count) * 100

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#fdf1e3')
    ax.set_facecolor('#fdf1e3')

    ax.barh(top_5_companies.index, top_5_percentages.values, color='#FF6F3C', edgecolor='#8B3A0E')
    ax.invert_yaxis()

    for i, (company, count, percentage) in enumerate(zip(top_5_companies.index, top_5_companies.values, top_5_percentages.values)):
        ax.text(percentage + 0.5, i, f'{count} ({percentage:.1f}%)', va='center', fontsize=10, color='purple', fontweight='bold')

    plt.title("Top 5 Best-selling Companies - Third Quarter / 2024", fontsize=18, fontweight='bold', color='#333333')
    plt.xlabel("Percentage (%)", fontsize=12, color='#4a4a4a', fontweight='bold')
    plt.ylabel("Company", fontsize=12, color='#4a4a4a', fontweight='bold')
    plt.xticks(np.arange(2, 21, 2), color='#4a4a4a')
    plt.yticks(color='#4a4a4a')
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.show()

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
        logo_label.image = logo_photo  # Lưu tham chiếu để tránh bị xóa bởi garbage collector
        logo_label.grid(row=0, column=0, padx=10, pady=10)
    except FileNotFoundError:
        messagebox.showerror("Error", "Logo file 'logo.png' not found.")

create_logo()


# Nút điều hướng
def create_nav_button(text, row, command=None):
    btn = tk.Button(sidebar, text=text, font=("Helvetica", 10, "bold"), fg="white", bg="#007bff", bd=0, padx=10, pady=10, command=command)
    btn.grid(row=row, column=0, sticky="ew", padx=10, pady=10)

create_nav_button("📂 Load Data", 1, load_data_from_csv)
create_nav_button("➕ Add Car", 2, open_input_window)
create_nav_button("🖉 Update Car", 3, update_car_by_id)
create_nav_button("📊 Show Chart", 4, show_chart)
create_nav_button("🗑 Delete Car", 5, delete_car)
create_nav_button("🚪 Quit", 6, quit_app)

# Khung chính
main_frame = tk.Frame(root, bg="#e6f7ff", padx=20, pady=20)
main_frame.pack(side="right", fill="both", expand=True)

# Tiêu đề
title_label = tk.Label(main_frame, text="CAR MANAGEMENT APP", font=("Helvetica", 24, 'bold'), bg="#e6f7ff", fg="green")
title_label.pack()

# Khung nhập liệu
input_frame = tk.Frame(main_frame, bg="#d9f2e6", padx=20, pady=20, bd=2, relief="groove")
input_frame.pack_forget()  # Ban đầu ẩn khung nhập liệu

# Khung bảng dữ liệu
table_frame = tk.Frame(main_frame, bg="#d9f2e6", bd=2, relief="groove")
table_frame.pack(fill="both", expand=True)

# Bảng dữ liệu
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)

# Thêm thanh cuộn dọc cho bảng dữ liệu
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

# Hiển thị dữ liệu ban đầu
view_data()

# Bắt đầu vòng lặp sự kiện Tkinter
root.mainloop()