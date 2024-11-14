import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

def show_chart():
    root = tk.Toplevel()
    root.title("Show Chart Options")
    window_width, window_height = 500, 550
    root.geometry(f"{window_width}x{window_height}")  # Thiết lập kích thước cửa sổ
    root.configure(bg="white")

    # Đặt cửa sổ ở giữa màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int((screen_height - window_height) / 2)
    position_left = int((screen_width - window_width) / 2)
    root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    # Đọc dữ liệu từ file data.csv
    try:
        car_data = pd.read_csv('../data/clean/Cleaned_Car_Dataset.csv').values.tolist()
    except FileNotFoundError:
        tk.messagebox.showerror("Lỗi", "File data.csv không tồn tại")
        return

    title_label = tk.Label(root, text="CHỌN BIỂU ĐỒ MUỐN HIỂN THỊ", font=("Arial", 20, "bold"), bg="white", fg="#003366")
    title_label.pack(pady=20)

    options = [
        ("Top 5 Thương hiệu bán chạy nhất", "1"),
        ("Top 5 Thương hiệu có doanh thu cao nhất", "2"),
        ("Top 5 Đại lý có doanh thu cao nhất", "3"),
        ("Phân phối màu sắc của xe", "4")
    ]

    selected_option = tk.StringVar(value="1")
    selected_button = None

    option_frame = tk.Frame(root, bg="white")
    option_frame.pack(pady=20)

    def on_select(e, value, button):
        nonlocal selected_button
        selected_option.set(value)
        if selected_button:
            selected_button.config(bg="#e0e0e0")
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
            show_top_dealers_chart(car_data)
        elif option == "4":
            show_color_distribution_chart(car_data)

    confirm_button = tk.Button(root, text="HIỂN THỊ", command=on_confirm, bg="#57a1f8", fg="white", font=('Arial', 14, 'bold'), padx=10, pady=10)
    confirm_button.pack(pady=20)

    root.transient()
    root.grab_set()
    root.wait_window(root)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int((screen_height - height) / 2)
    position_left = int((screen_width - width) / 2)
    window.geometry(f"{width}x{height}+{position_left}+{position_top}")


def show_top_dealers_chart(car_data):
   
    # Tạo cửa sổ hiển thị biểu đồ
    chart_window = tk.Toplevel()
    chart_window.title("Top 5 Dealer Revenue")
    center_window(chart_window, 1000, 800)  # Center window (giữ nguyên nếu bạn đã định nghĩa)

    # Tính tổng doanh thu theo đại lý
    from collections import defaultdict
    dealer_revenue = defaultdict(int)
    for car in car_data:
        dealer_revenue[car[5]] += car[9]
    
    # Lấy top 5 đại lý có doanh thu cao nhất
    top_dealers = sorted(dealer_revenue.items(), key=lambda x: x[1], reverse=True)[:5]
    dealers, revenues = zip(*top_dealers)

    # Tạo biểu đồ cột
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(dealers, revenues, color='skyblue')
    ax.set_title("Top 5 Dealer Revenue", fontsize=14)
    ax.set_xlabel("Dealer Name", fontsize=12)
    ax.set_ylabel("Total Revenue", fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.set_xticks(range(len(dealers)))
    ax.set_xticklabels(dealers, rotation=0, fontsize=8, ha='center')

    # Hiển thị doanh thu trên từng cột
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', 
                ha='center', va='bottom', fontsize=10)

    # Kết nối với tkinter
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
    center_window(chart_window, 800, 600)

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
    center_window(chart_window, 600, 600)

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
    center_window(chart_window, 600, 600)

    fig, ax = plt.subplots(figsize=(6, 6))
    labels = color_count.keys()
    sizes = color_count.values()
    
    ax.pie(sizes, labels=[f"{label} ({count})" for label, count in zip(labels, sizes)],
           autopct='%1.1f%%', startangle=140)
    
    ax.set_title("Phân Bố Màu Sắc Các Loại Xe")

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
