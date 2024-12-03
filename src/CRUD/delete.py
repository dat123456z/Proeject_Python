from tkinter import messagebox
from CRUD.create import save_data_to_csv
from CRUD.sort import view_data

def delete_car(columns, car_data, tree=None):
    # Lấy các item được chọn trong treeview
    selected_items = tree.selection()
    
    # Kiểm tra nếu không có dòng nào được chọn
    if not selected_items:
        messagebox.showwarning("Error", "Please select one or more rows to delete.")
        return

    # Tạo danh sách các ID của các dòng được chọn
    selected_ids = []
    for item in selected_items:
        try:
            selected_id = tree.item(item, "values")[0]  # Giả sử ID nằm ở cột đầu tiên
            selected_ids.append(str(selected_id))
        except IndexError:
            messagebox.showerror("Error", "Unable to determine ID from selected row.")
            return

    # Xác nhận xóa
    confirm = messagebox.askyesno("Confirm deletion", f"Are you sure you want to delete the data with ID: {', '.join(selected_ids)}?")
    if confirm:
        try:
            # Duyệt qua từng ID đã chọn và xóa dòng tương ứng trong car_data
            for selected_id in selected_ids:
                for row in car_data:
                    if str(row[0]) == selected_id:  # Kiểm tra nếu ID trong car_data trùng với selected_id
                        car_data.remove(row)  # Sử dụng remove() để xóa dòng

            # Lưu lại dữ liệu vào CSV sau khi xóa
            save_data_to_csv(columns=columns, car_data=car_data)
            
            # Cập nhật lại giao diện table view
            view_data(tree=tree, car_data=car_data)
            
            messagebox.showinfo("Success", f"Deleted data with ID: {', '.join(selected_ids)}.")
        except Exception as e:
            messagebox.showerror("Error", f"An Error Occurred: {str(e)}")


