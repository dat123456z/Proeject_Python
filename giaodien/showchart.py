import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

def show_chart():
    root = tk.Toplevel()
    root.title("Show Chart Options")
    root.geometry("400x500")
    root.configure(bg="white")

    # Đọc dữ liệu từ file data.csv
    try:
        car_data = pd.read_csv('data.csv').values.tolist()
    except FileNotFoundError:
        tk.messagebox.showerror("Lỗi", "File data.csv không tồn tại")
        return

    title_label = tk.Label(root, text="CHỌN BIỂU ĐỒ MUỐN HIỂN THỊ", font=("Arial", 20, "bold"), bg="white", fg="#003366")
    title_label.pack(pady=20)

    options = [
        ("Top 5 Best-selling Brands", "1"),
        ("Top 5 Highest Revenue Brands", "2"),
        ("Customer Gender Distribution", "3"),
        ("Color Distribution of Cars", "4")
    ]

    selected_option = tk.StringVar(value="1")
    selected_button = None  # Để lưu ô được chọn hiện tại

    option_frame = tk.Frame(root, bg="white")
    option_frame.pack(pady=20)

    def on_select(e, value, button):
        nonlocal selected_button
        selected_option.set(value)

        # Đặt màu nền bình thường cho ô trước đó
        if selected_button:
            selected_button.config(bg="#e0e0e0")

        # Đặt màu nền đậm cho ô được chọn
        button.config(bg="#cce7ff")
        selected_button = button

    for text, value in options:
        option_button = tk.Label(option_frame, text=text, font=("Arial", 14), bg="#e0e0e0", fg="#003366", width=30, height=2, padx=10, pady=5)
        option_button.pack(pady=5, fill="x")
        option_button.bind("<Button-1>", lambda e, v=value, btn=option_button: on_select(e, v, btn))

    def on_confirm():
        option = selected_option.get()
        root.destroy()
        if option == "1":
            show_top_5_brands_chart(car_data)
        elif option == "2":
            show_top_5_revenue_chart(car_data)
        elif option == "3":
            show_gender_chart(car_data)
        elif option == "4":
            show_color_distribution_chart(car_data)

    confirm_button = tk.Button(root, text="HIỂN THỊ", command=on_confirm, bg="#57a1f8", fg="white", font=('Arial', 14, 'bold'), padx=10, pady=10)
    confirm_button.pack(pady=20)

    root.transient()
    root.grab_set()
    root.wait_window(root)

# Các hàm biểu đồ bên dưới đều thêm `root` và `car_data` làm tham số
# Đoạn mã biểu đồ không thay đổi ở đây



# Các hàm biểu đồ bên dưới đều thêm `root` và `car_data` làm tham số

def show_gender_chart(car_data):
    chart_window = tk.Toplevel()
    chart_window.title("Biểu đồ giới tính")
    chart_window.geometry("600x600")

    male_count = sum(1 for car in car_data if car[3] == "Male")
    female_count = sum(1 for car in car_data if car[3] == "Female")

    fig, ax = plt.subplots(figsize=(6, 6))
    labels = ["Male", "Female"]
    sizes = [male_count, female_count]
    ax.pie(sizes, labels=[f"{label} ({count})" for label, count in zip(labels, sizes)],
           autopct='%1.1f%%', startangle=140, colors=['lightblue', 'pink'])
    ax.set_title("Giới Tính khách hàng")

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def show_top_5_brands_chart(car_data):
    brands = [car[6] for car in car_data]
    brand_count = {}
    for brand in brands:
        brand_count[brand] = brand_count.get(brand, 0) + 1
    top_5_brands = sorted(brand_count.items(), key=lambda x: x[1], reverse=True)[:5]
    total_cars_sold = sum(brand_count.values())

    companies = [item[0] for item in top_5_brands]
    counts = [item[1] for item in top_5_brands]
    percentages = [f"{(count / total_cars_sold) * 100:.2f}%" for count in counts]

    chart_window = tk.Toplevel()
    chart_window.title("Top 5 Hãng Xe Bán Chạy Nhất")
    chart_window.geometry("800x600")

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(companies, counts, color="green")

    ax.set_title("Top 5 Best-selling Companies - Third Quarter / 2024", fontsize=16, weight='bold')
    ax.set_xlabel("Company", fontsize=12)
    ax.set_ylabel("Number of Cars Sold", fontsize=12)

    for i, (bar, percent) in enumerate(zip(bars, percentages)):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), percent, 
                ha='center', va='bottom', fontsize=10, color="purple", fontweight="bold")

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def show_top_5_revenue_chart(car_data):
    revenue_data = {}
    for car in car_data:
        brand = car[6]
        price = int(car[9])
        revenue_data[brand] = revenue_data.get(brand, 0) + price
    top_5_revenue = sorted(revenue_data.items(), key=lambda x: x[1], reverse=True)[:5]

    chart_window = tk.Toplevel()
    chart_window.title("Top 5 Hãng Xe Có Doanh Thu Cao Nhất")
    chart_window.geometry("600x600")

    fig, ax = plt.subplots(figsize=(8, 6))
    companies = [item[0] for item in top_5_revenue]
    revenues = [item[1] for item in top_5_revenue]
    bars = ax.bar(companies, revenues, color="gold")

    ax.set_title("Top 5 Hãng Xe Có Doanh Thu Cao Nhất", fontsize=16, weight='bold')
    ax.set_xlabel("Hãng Xe", fontsize=12)
    ax.set_ylabel("Doanh Thu", fontsize=12)

    for bar, revenue in zip(bars, revenues):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{revenue:,}", 
                ha='center', va='bottom', fontsize=10, color="black", fontweight="bold")

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def show_color_distribution_chart(car_data):
    colors = [car[8] for car in car_data]
    color_count = {}
    for color in colors:
        color_count[color] = color_count.get(color, 0) + 1

    chart_window = tk.Toplevel()
    chart_window.title("Phân Bố Màu Sắc Các Loại Xe")
    chart_window.geometry("600x600")

    fig, ax = plt.subplots(figsize=(6, 6))
    labels = color_count.keys()
    sizes = color_count.values()
    
    ax.pie(sizes, labels=[f"{label} ({count})" for label, count in zip(labels, sizes)],
           autopct='%1.1f%%', startangle=140)
    
    ax.set_title("Phân Bố Màu Sắc Các Loại Xe")

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
