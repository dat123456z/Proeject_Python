import csv
from tkinter import messagebox
from module.module import view_data

def load_data_from_csv(car_data, tree, input_frame, table_frame):
    input_frame.pack_forget()  # Ẩn khung nhập liệu
    table_frame.pack(fill="both", expand=True)  # Hiển thị lại khung bảng dữ liệu

    file_path = 'data/clean/Cleaned_Car_Dataset.csv'
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            car_data.clear()
            for row in reader:
                car_data.append(row)
        view_data(tree= tree, car_data=car_data)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{file_path}' not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")