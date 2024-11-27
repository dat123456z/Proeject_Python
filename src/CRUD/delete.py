from tkinter import messagebox
from CRUD.create import save_data_to_csv
from CRUD.sort import view_data

def delete_car(columns, car_data, tree=None):
    # Lấy item được chọn trong treeview
    selected_item = tree.selection()
    
    # Kiểm tra nếu không có dòng nào được chọn
    if not selected_item:
        messagebox.showwarning("Error", "Please select a row to delete")
        return

    # Lấy ID của dòng được chọn
    try:
        selected_id = tree.item(selected_item[0], "values")[0]  # Giả sử ID nằm ở cột đầu tiên
    except IndexError:
        messagebox.showerror("Error", "Unable to determine ID from selected row")
        return

    # Xác nhận xóa
    confirm = messagebox.askyesno("Confirm deletion", f"Are you sure you want to delete data with ID: {selected_id}?")
    if confirm:
        try:
            # Tìm dòng có ID khớp trong car_data
            row_to_delete = next((row for row in car_data if str(row[0]) == str(selected_id)), None)
            
            if row_to_delete:
                car_data.remove(row_to_delete)  # Xóa dòng khỏi danh sách
                
                # Lưu lại dữ liệu vào CSV sau khi xóa
                save_data_to_csv(columns=columns, car_data=car_data)
                
                # Cập nhật lại giao diện table view
                view_data(tree=tree, car_data=car_data)
                
                messagebox.showinfo("Delete successful", f"Deleted data with ID: {selected_id}.")
            else:
                messagebox.showerror("Error", f"No data found with ID: {selected_id}.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")