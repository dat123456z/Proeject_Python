import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

def show_chart_options():
    # Tạo cửa sổ mới với kích thước lớn hơn
    chart_window = tk.Toplevel(root)
    chart_window.title("Show Chart Options")
    chart_window.geometry("800x600")  # Thiết lập kích thước cửa sổ lớn hơn

    # Tạo tiêu đề
    title_label = tk.Label(chart_window, text="Chọn yêu cầu muốn thực hiện:", font=("Arial", 25, "bold"))
    title_label.pack(pady=18)

    # Các tùy chọn biểu đồ
    options = [
        ("1. Biểu đồ top 5 hãng xe bán chạy nhất", "1"),
        ("2. Biểu đồ top 5 hãng xe có doanh thu cao nhất ", "2"),
        ("3. Biểu đồ giới tính của khách hàng", "3"),
        ("4. Biểu đồ màu sắc của các loại xe được mua", "4")
    ]

    selected_option = tk.StringVar(value="1")  # Giá trị mặc định là 1
    for text, value in options:
        tk.Radiobutton(chart_window, text=text, variable=selected_option, value=value, font=("Arial", 18)).pack(anchor="w", padx=20)

    # Nút xác nhận
    def on_confirm():
        option = selected_option.get()
        chart_window.destroy()  # Đóng cửa sổ khi chọn
        if option == "1":
           show_top_5_brands_chart()
        elif option == "2":
            show_top_5_revenue_chart()
        elif option == "3":
            show_gender_chart()
        elif option=="4":
            show_color_distribution_chart()
        else:
            tk.messagebox.showwarning("Invalid Option", "Vui lòng chọn 1, 2 hoặc 3.")
    
    confirm_button = tk.Button(chart_window, text="OK", command=on_confirm, bg="#57a1f8", fg="white", font=('Arial', 18, 'bold'), padx=20, pady=5)
    confirm_button.pack(pady=20)

    chart_window.transient(root)  # Đặt cửa sổ này trên cùng của cửa sổ chính
    chart_window.grab_set()  # Đặt focus vào cửa sổ mới để người dùng phải chọn trước khi tiếp tục
    root.wait_window(chart_window)  # Đợi cho đến khi cửa sổ mới được đóng



def show_gender_chart():
    # Tạo cửa sổ riêng cho biểu đồ
    chart_window = tk.Toplevel(root)
    chart_window.title("Biểu đồ giới tính")
    chart_window.geometry("600x600")  # Kích thước của cửa sổ biểu đồ

    male_count = sum(1 for car in car_data if car[3] == "Male")
    female_count = sum(1 for car in car_data if car[3] == "Female")

    # Tạo biểu đồ trong cửa sổ con
    fig, ax = plt.subplots(figsize=(6, 6))
    labels = ["Male", "Female"]
    sizes = [male_count, female_count]
    ax.pie(sizes, labels=[f"{label} ({count})" for label, count in zip(labels, sizes)],
           autopct='%1.1f%%', startangle=140, colors=['lightblue', 'pink'])
    ax.set_title("Giới Tính khách hàng")

    # Hiển thị biểu đồ trong cửa sổ mới
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# Phần bổ sung cho các hàm biểu đồ
def show_top_5_brands_chart():
    # Lấy dữ liệu các hãng xe và đếm số lượng xe của từng hãng
    brands = [car[6] for car in car_data]
    brand_count = {}
    for brand in brands:
        brand_count[brand] = brand_count.get(brand, 0) + 1
    top_5_brands = sorted(brand_count.items(), key=lambda x: x[1], reverse=True)[:5]

    # Tính tổng số xe bán được của tất cả các hãng
    total_cars_sold = sum(brand_count.values())

    # Chuẩn bị dữ liệu cho biểu đồ
    companies = [item[0] for item in top_5_brands]
    counts = [item[1] for item in top_5_brands]
    percentages = [f"{(count / total_cars_sold) * 100:.2f}%" for count in counts]  # Tính phần trăm với 2 chữ số thập phân

    # Hiển thị biểu đồ cột cho top 5 hãng xe bán chạy nhất
    chart_window = tk.Toplevel(root)
    chart_window.title("Top 5 Hãng Xe Bán Chạy Nhất")
    chart_window.geometry("800x600")

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(companies, counts, color="green")

    # Đặt tiêu đề và nhãn
    ax.set_title("Top 5 Best-selling Companies - Third Quarter / 2024", fontsize=16, weight='bold')
    ax.set_xlabel("Company", fontsize=12)
    ax.set_ylabel("Number of Cars Sold", fontsize=12)

    # Hiển thị phần trăm trên mỗi cột
    for i, (bar, percent) in enumerate(zip(bars, percentages)):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), percent, 
                ha='center', va='bottom', fontsize=10, color="purple", fontweight="bold")

    # Hiển thị biểu đồ trong cửa sổ mới
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def show_top_5_revenue_chart():
    # Lấy dữ liệu doanh thu theo hãng xe và tính tổng doanh thu
    revenue_data = {}
    for car in car_data:
        brand = car[6]
        price = int(car[9])
        revenue_data[brand] = revenue_data.get(brand, 0) + price
    top_5_revenue = sorted(revenue_data.items(), key=lambda x: x[1], reverse=True)[:5]

    # Hiển thị biểu đồ cột cho top 5 hãng xe có doanh thu cao nhất
    chart_window = tk.Toplevel(root)
    chart_window.title("Top 5 Hãng Xe Có Doanh Thu Cao Nhất")
    chart_window.geometry("600x600")

    fig, ax = plt.subplots(figsize=(8, 6))
    companies = [item[0] for item in top_5_revenue]
    revenues = [item[1] for item in top_5_revenue]

    # Tạo biểu đồ cột với màu vàng
    bars = ax.bar(companies, revenues, color="gold")

    # Đặt tiêu đề và nhãn
    ax.set_title("Top 5 Hãng Xe Có Doanh Thu Cao Nhất", fontsize=16, weight='bold')
    ax.set_xlabel("Hãng Xe", fontsize=12)
    ax.set_ylabel("Doanh Thu", fontsize=12)

    # Hiển thị doanh thu trên mỗi cột
    for bar, revenue in zip(bars, revenues):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{revenue:,}", 
                ha='center', va='bottom', fontsize=10, color="black", fontweight="bold")

    # Hiển thị biểu đồ trong cửa sổ mới
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)



def show_color_distribution_chart():
    # Lấy dữ liệu màu sắc và đếm số lượng xe của từng màu
    colors = [car[8] for car in car_data]
    color_count = {}
    for color in colors:
        color_count[color] = color_count.get(color, 0) + 1

    # Hiển thị biểu đồ tròn cho phân bố màu sắc của các loại xe
    chart_window = tk.Toplevel(root)
    chart_window.title("Phân Bố Màu Sắc Các Loại Xe")
    chart_window.geometry("600x600")

    fig, ax = plt.subplots(figsize=(6, 6))
    labels = color_count.keys()
    sizes = color_count.values()
    
    # Tạo biểu đồ tròn và hiển thị số lượng trên mỗi phần của biểu đồ
    ax.pie(sizes, labels=[f"{label} ({count})" for label, count in zip(labels, sizes)],
           autopct='%1.1f%%', startangle=140)
    
    ax.set_title("Phân Bố Màu Sắc Các Loại Xe")

    # Hiển thị biểu đồ trong cửa sổ mới
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


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
create_nav_button("📊 Show Chart", 4, show_chart_options)
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

