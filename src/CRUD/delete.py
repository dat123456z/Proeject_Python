from tkinter import messagebox
from CRUD.create import save_data_to_csv
from module.module import view_data

def delete_car(columns, car_data, tree=None):
    # Lấy item được chọn trong treeview
    selected_item = tree.selection()
    
    # Kiểm tra nếu không có dòng nào được chọn
    if not selected_item:
        messagebox.showwarning("Lỗi", "Vui lòng chọn một dòng để xóa.")
        return

    # Lấy ID của dòng được chọn
    try:
        selected_id = tree.item(selected_item[0], "values")[0]  # Giả sử ID nằm ở cột đầu tiên
    except IndexError:
        messagebox.showerror("Lỗi", "Không thể xác định ID từ dòng được chọn.")
        return

    # Xác nhận xóa
    confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa dữ liệu với ID: {selected_id}?")
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
                
                messagebox.showinfo("Thành công", f"Đã xóa dữ liệu với ID: {selected_id}.")
            else:
                messagebox.showerror("Lỗi", f"Không tìm thấy dữ liệu với ID: {selected_id}.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")