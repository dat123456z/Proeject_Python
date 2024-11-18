from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from CRUD.create import save_data_to_csv
from CRUD.sort import view_data


def check_car_exists(car_id, car_data):
    for car in car_data:
        if car[0] == car_id:
            return True
    return False

def update_car(car_id, car_data, table_frame, input_frame, columns, tree):
    for car in car_data:
        if car[0] == car_id:
            open_input_window_for_update(car_id, table_frame, input_frame, columns, car_data, tree)
            return
    messagebox.showerror("Error", "Car ID not found.")

def update_car_by_id(root, car_data, table_frame, input_frame, columns, tree):
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
        open_input_window_for_update(car_id, table_frame, input_frame, columns, car_data, tree)

    ttk.Button(update_window, text="Cập nhật", command=check_and_update).pack(pady=10)

def open_input_window_for_update(car_id, table_frame, input_frame, columns, car_data, tree):
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

    save_button = tk.Button(input_frame, text="Save", command=lambda: save_updated_car(car_id, columns, car_data, tree, input_frame, table_frame), bg="#007bff", fg="white", font=('Helvetica', 10, 'bold'), bd=0, padx=20, pady=5)
    save_button.grid(row=len(columns), column=0, columnspan=2, pady=10)

def save_updated_car(car_id, columns, car_data, tree, input_frame, table_frame):
    updated_car = []
    new_car_id = entries["Car_id"].get()

    # Kiểm tra nếu Car_id mới đã tồn tại trong dữ liệu (ngoại trừ bản ghi hiện tại)
    if new_car_id != car_id and check_car_exists(new_car_id , car_data):
        messagebox.showerror("Lỗi", "ID xe đã tồn tại. Vui lòng nhập ID khác.")
        entries["Car_id"].focus_set()  # Đặt con trỏ vào Car ID để nhập lại
        return

    for col in columns:
        value = entries[col].get()
        if not value:
            messagebox.showwarning("Lỗi nhập liệu", "Vui lòng điền vào đầy đủ dữ liệu.")
            return
        updated_car.append(value)

    # Cập nhật dữ liệu với Car_id mới và lưu lại
    for i, car in enumerate(car_data):
        if car[0] == car_id:
            car_data[i] = updated_car
            break

    save_data_to_csv(columns=columns, car_data=car_data)
    input_frame.pack_forget()
    table_frame.pack(fill="both", expand=True)
    view_data(tree= tree, car_data=car_data)
    messagebox.showinfo("", "Cập nhật dữ liệu thành công.")