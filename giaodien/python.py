import tkinter as tk
from tkinter import ttk, messagebox
import csv
import matplotlib.pyplot as plt

# Data storage
car_data = []

# Hàm mở cửa sổ nhập dữ liệu
def open_input_window():
    # Ẩn bảng dữ liệu và hiển thị khung nhập liệu
    table_frame.pack_forget()
    input_frame.pack(fill="x", pady=20)

    # Hiển thị khung nhập liệu
    for widget in input_frame.winfo_children():
        widget.destroy()  # Xóa các widget cũ trong input_frame

    # Tạo các trường nhập liệu cho mỗi cột
    global entries
    entries = {}
    for idx, col in enumerate(columns):
        label = tk.Label(input_frame, text=col, font=('Helvetica', 10, 'bold'), fg="#ffffff", bg="#3b3b3b")
        label.grid(row=idx, column=0, sticky='w', padx=10, pady=8)
        entry = ttk.Entry(input_frame, width=50)
        entry.grid(row=idx, column=1, padx=10, pady=8)
        entries[col] = entry

    # Nút lưu dữ liệu
    save_button = tk.Button(input_frame, text="Save", command=save_and_view_data, bg="#57a1f8", fg="white", font=('Helvetica', 10, 'bold'), bd=0, padx=20, pady=5)
    save_button.grid(row=len(columns), column=0, columnspan=2, pady=10)

def save_and_view_data():
    car_id = entries["Car_id"].get()
    if check_car_exists(car_id):
        update_car(car_id)
    else:
        add_car()
    # Hiển thị bảng dữ liệu sau khi thêm hoặc cập nhật
    input_frame.pack_forget()
    table_frame.pack(fill="both", expand=True)
    view_data()

def check_car_exists(car_id):
    # Kiểm tra xem Car_id đã tồn tại trong car_data chưa
    for car in car_data:
        if car[0] == car_id:
            return True
    return False

def load_data_from_csv():
    # Load dữ liệu từ tệp CSV
    file_path = 'data.csv'
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Bỏ qua hàng tiêu đề
            car_data.clear()
            for row in reader:
                car_data.append(row)
        view_data()
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{file_path}' not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")

def view_data():
    # Xóa dữ liệu cũ và hiển thị dữ liệu mới
    for row in tree.get_children():
        tree.delete(row)
    for row in car_data:
        tree.insert("", tk.END, values=row)

def add_car():
    # Lấy dữ liệu từ các trường nhập liệu
    new_car = []
    for col in columns:
        value = entries[col].get()
        if not value:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        new_car.append(value)

    # Thêm dữ liệu mới vào danh sách car_data
    car_data.append(new_car)
    
    # Thêm dữ liệu vào treeview
    tree.insert("", tk.END, values=new_car)

    # Ghi dữ liệu mới vào file CSV
    save_data_to_csv()

    # Xóa các trường nhập liệu sau khi lưu
    for entry in entries.values():
        entry.delete(0, tk.END)

def update_car(car_id):
    # Cập nhật thông tin của xe với Car_id đã tồn tại
    updated_car = []
    for col in columns:
        value = entries[col].get()
        if not value:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        updated_car.append(value)
    
    # Tìm và cập nhật dữ liệu trong car_data
    for i, car in enumerate(car_data):
        if car[0] == car_id:
            car_data[i] = updated_car
            break

    # Ghi dữ liệu mới vào file CSV
    save_data_to_csv()

    # Xóa các trường nhập liệu sau khi cập nhật
    for entry in entries.values():
        entry.delete(0, tk.END)

def save_data_to_csv():
    # Lưu toàn bộ dữ liệu hiện tại vào file CSV
    file_path = 'data.csv'
    try:
        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)  # Ghi tiêu đề cột
            writer.writerows(car_data)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

def update_car_by_selection():
    # Lấy dữ liệu từ hàng được chọn và điền vào khung nhập liệu
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No selection", "Please select a row to update.")
        return

    car_id = tree.item(selected_item[0])['values'][0]
    for car in car_data:
        if car[0] == car_id:
            open_input_window()
            for idx, col in enumerate(columns):
                entries[col].insert(0, car[idx])
            break

def delete_car():
    # Xóa dữ liệu được chọn
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
    # Tạo biểu đồ dựa trên dữ liệu Annual Income
    if not car_data:
        messagebox.showwarning("No Data", "No data available to display chart.")
        return

    # Lấy danh sách tên khách hàng và thu nhập
    customer_names = [car[2] for car in car_data]  # Tên khách hàng
    incomes = [float(car[4]) for car in car_data]  # Thu nhập hàng năm (Annual Income)

    plt.figure(figsize=(10, 6))
    plt.bar(customer_names, incomes, color='skyblue')
    plt.xlabel("Customer Name")
    plt.ylabel("Annual Income")
    plt.title("Annual Income of Customers")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def quit_app():
    root.quit()

# Giao diện chính
root = tk.Tk()
root.title("Car Management System")
root.geometry("1500x700")
root.configure(bg="#2e2e2e")

# Thanh điều hướng bên trái
sidebar = tk.Frame(root, bg="#292929", width=100, height=700)
sidebar.pack(side="left", fill="y")

# Nút điều hướng với biểu tượng
def create_nav_button(text, row, command=None):
    btn = tk.Button(sidebar, text=text, font=("Helvetica", 10, "bold"), fg="#57a1f8", bg="#333333", bd=0, padx=10, pady=10, command=command)
    btn.grid(row=row, column=0, sticky="ew", padx=10, pady=10)

create_nav_button("📂 Load CSV", 0, load_data_from_csv)
create_nav_button("➕ Add Car", 1, open_input_window)
create_nav_button("🖉 Update Car", 2, update_car_by_selection)
create_nav_button("📊 Show Chart", 3, show_chart)  # Nút để hiển thị biểu đồ
create_nav_button("🗑 Delete Car", 4, delete_car)
create_nav_button("🚪 Quit", 5, quit_app)

# Khung chính
main_frame = tk.Frame(root, bg="#1e1e2e", padx=20, pady=20)
main_frame.pack(side="right", fill="both", expand=True)

# Tiêu đề
title_label = tk.Label(main_frame, text="Car Management App", font=("Helvetica", 24, 'bold'), bg="#1e1e2e", fg="#ffffff")
title_label.pack()

# Khung nhập liệu dạng thẻ
input_frame = tk.Frame(main_frame, bg="#3b3b3b", padx=20, pady=20, bd=2, relief="groove")
input_frame.pack_forget()  # Ban đầu ẩn khung nhập liệu

# Khung bảng dữ liệu
table_frame = tk.Frame(main_frame, bg="#2e2e2e", bd=2, relief="groove")
table_frame.pack(fill="both", expand=True)

# Bảng dữ liệu với màu nền và tiêu đề đậm
columns = ["Car_id", "Date", "Customer Name", "Gender", "Annual Income", "Dealer_Name", "Company", "Model", "Color", "Price", "Phone"]
tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Custom.Treeview")

# Tạo tiêu đề và độ rộng cho từng cột
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)

# Thêm thanh cuộn dọc cho bảng
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

# Hiển thị dữ liệu ban đầu
view_data()

root.mainloop()
