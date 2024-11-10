from tkinter import messagebox
from src.CRUD.create import save_data_to_csv
from src.module.module import view_data

def delete_car(columns, car_data, tree = None):
    # Lấy item được chọn trong treeview
    selected_item = tree.selection()
    
    # Kiểm tra nếu không có dòng nào được chọn
    if not selected_item:
        messagebox.showwarning("Lỗi", "Vui lòng chọn một dòng để xóa.")
        return

    # Xác nhận xóa
    confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn xóa cột được chọn không?")
    
    if confirm:
        try:
            # Lấy chỉ số dữ liệu từ item trong tree
            data_index = tree.index(selected_item[0])
            
            # Xóa dữ liệu từ car_data
            del car_data[data_index]
            
            # Lưu lại dữ liệu vào CSV sau khi xóa
            save_data_to_csv(columns=columns, car_data=car_data)
            
            # Cập nhật lại giao diện table view
            view_data(tree=tree, car_data=car_data)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
