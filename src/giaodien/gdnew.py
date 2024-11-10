import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.giaodien.showchart import show_chart
from src.CRUD.create import save_data_to_csv, add_car
from src.module.module import sort_column, view_data
from src.CRUD.read import load_data_from_csv
from src.CRUD.delete import delete_car
from src.CRUD.update import *


def giaodien():
        
    # Data storage
    car_data = []
    columns = ["Car_id", "Date", "Customer Name", "Gender", "Annual Income", "Dealer_Name", "Company", "Model", "Color", "Price", "Phone"]

    # Tạo từ điển để lưu trạng thái sắp xếp cho từng cột (True là giảm dần, False là tăng dần)
    sort_states = {col: False for col in columns}

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
        if check_car_exists(car_id, car_data=car_data):
            id_warning_label.config(text="ID đã tồn tại.", fg="green")  # Hiển thị cảnh báo nếu ID tồn tại
        else:
            id_warning_label.config(text="")  # Ẩn cảnh báo nếu ID chưa tồn tại

    def save_and_view_data():
        car_id = entries["Car_id"].get()
        if check_car_exists(car_id, car_data=car_data):
            messagebox.showerror("Lỗi", "ID xe đã tồn tại. Vui lòng nhập ID khác")
            entries["Car_id"].delete(0, tk.END)
            entries["Car_id"].focus_set()  # Đặt con trỏ vào Car ID để nhập lại
        else:
            if add_car(columns, entries, car_data, tree, input_frame, table_frame):  # Gọi add_car và chỉ ẩn input_frame nếu thêm thành công
                input_frame.pack_forget()
                table_frame.pack(fill="both", expand=True)
                view_data(tree= tree, car_data=car_data)

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

    create_nav_button("📂 Load Data", 1, lambda: load_data_from_csv(car_data, tree, input_frame, table_frame))
    create_nav_button("➕ Add Car", 2, open_input_window)
    create_nav_button("🖉 Update Car", 3, lambda: update_car_by_id(root, car_data, table_frame, input_frame, columns, tree))
    create_nav_button("🗑 Delete Car", 4, lambda: delete_car(columns, car_data, tree))
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
        tree.heading(col, text=col, command=lambda _col=col: sort_column(_col,columns, sort_states, car_data, tree))
        tree.column(col, anchor="center", width=120)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    load_data_from_csv(car_data, tree, input_frame, table_frame)
    view_data(tree= tree, car_data=car_data)

    # Bắt đầu vòng lặp sự kiện Tkinter
    root.mainloop()

