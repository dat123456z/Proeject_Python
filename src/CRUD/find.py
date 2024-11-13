from tkinter import messagebox
def search_by_company(search_entry, columns, car_data, tree, pagination_frame):
    """Tìm kiếm xe theo công ty."""
    search_term = search_entry.get().strip().lower()
    
    if not search_term:
        messagebox.showwarning("Warning", "Please enter a company name to search.")
        return

    # Lọc dữ liệu theo cột "Company"
    filtered_data = [car for car in car_data if search_term in car[columns.index("Company")].strip().lower()]

    # Hiển thị thông báo nếu không có dữ liệu
    if not filtered_data:
        messagebox.showinfo("Info", "No cars found for the specified company.")
        return

    # Làm sạch bảng và hiển thị kết quả lọc
    for row in tree.get_children():
        tree.delete(row)

    for row in filtered_data:
        tree.insert("", "end", values=row)
