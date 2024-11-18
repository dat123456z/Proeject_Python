import tkinter as tk # Thư viện giao diện đồ họa
from tkinter import ttk, messagebox # Thư viện giao diện đồ họa
import csv # Thư viện xử lý file CSV
import os # Thư viện xử lý hệ thống
from PIL import Image, ImageTk # Thư viện xử lý ảnh
from giaodien.showchart import show_chart   # Thư viện xử lý biểu đồ
from CRUD.create import save_data_to_csv, add_car # Thư viện xử lý tạo mới
from CRUD.sort import sort_column # Thư viện xử lý sắp xếp và xem dữ liệu
from CRUD.read import load_data_from_csv # Thư viện xử lý đọc dữ liệu từ file CSV
from CRUD.delete import delete_car # Thư viện xử lý xóa dữ liệu
from CRUD.update import * # Thư viện xử lý cập nhật dữ liệu
from CRUD.find import search_by_company # Thư viện xử lý tìm kiếm dữ liệu

# Số lượng mục trên mỗi trang
ITEMS_PER_PAGE = 100

# Biến lưu trạng thái trang hiện tại
current_page = 0

def update_pagination(tree, car_data, pagination_frame, page):
    """Cập nhật dữ liệu hiển thị trên Treeview theo trang."""
    global current_page
    current_page = page

    # Làm sạch dữ liệu trong Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Lấy dữ liệu thuộc trang hiện tại
    start_index = page * ITEMS_PER_PAGE
    end_index = min(start_index + ITEMS_PER_PAGE, len(car_data))
    page_data = car_data[start_index:end_index]

    # Hiển thị dữ liệu trên Treeview
    for row in page_data:
        tree.insert("", "end", values=row)

    # Cập nhật trạng thái của các nút phân trang
    update_pagination_buttons(tree, pagination_frame, car_data, page)

def update_pagination_buttons(tree, pagination_frame, car_data, page):
    """Cập nhật trạng thái các nút phân trang."""
    for widget in pagination_frame.winfo_children():
        widget.destroy()

    total_pages = (len(car_data) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    # Nút "Trang trước"
    if page > 0:
        prev_button = tk.Button(pagination_frame, text="<", command=lambda: update_pagination(tree, car_data, pagination_frame, page - 1))
        prev_button.pack(side="left", padx=2)

    # Hiển thị các số trang
    MAX_VISIBLE_PAGES = 5  # Số trang tối đa hiển thị (cả 2 bên)
    start_page = max(0, page - MAX_VISIBLE_PAGES // 2)
    end_page = min(total_pages, start_page + MAX_VISIBLE_PAGES)

    # Điều chỉnh để không bị cắt trang cuối
    if end_page - start_page < MAX_VISIBLE_PAGES:
        start_page = max(0, end_page - MAX_VISIBLE_PAGES)

    if start_page > 0:
        first_page_button = tk.Button(pagination_frame, text="1", command=lambda: update_pagination(tree, car_data, pagination_frame, 0))
        first_page_button.pack(side="left", padx=2)

        if start_page > 1:
            dots_label = tk.Label(pagination_frame, text="...", bg="#e6f7ff")
            dots_label.pack(side="left", padx=2)

    for p in range(start_page, end_page):
        page_button = tk.Button(
            pagination_frame,
            text=str(p + 1),
            bg="#007bff" if p == page else "#e6f7ff",
            fg="white" if p == page else "black",
            command=lambda p=p: update_pagination(tree, car_data, pagination_frame, p),
        )
        page_button.pack(side="left", padx=2)

    if end_page < total_pages:
        if end_page < total_pages - 1:
            dots_label = tk.Label(pagination_frame, text="...", bg="#e6f7ff")
            dots_label.pack(side="left", padx=2)

        last_page_button = tk.Button(pagination_frame, text=str(total_pages), command=lambda: update_pagination(tree, car_data, pagination_frame, total_pages - 1))
        last_page_button.pack(side="left", padx=2)

    # Nút "Trang sau"
    if page < total_pages - 1:
        next_button = tk.Button(pagination_frame, text=">", command=lambda: update_pagination(tree, car_data, pagination_frame, page + 1))
        next_button.pack(side="left", padx=2)

def giaodien():
    # Data storage
    car_data = []
    columns = ["Car_id", "Date", "Customer Name", "Gender", "Annual Income", "Dealer_Name", "Company", "Model", "Color", "Price", "Phone"]

    # Tạo từ điển để lưu trạng thái sắp xếp cho từng cột (True là giảm dần, False là tăng dần)
    sort_states = {col: False for col in columns}

    def open_input_window():
        table_frame.pack_forget()
        input_frame.pack(fill="x", pady=20)

        for widget in input_frame.winfo_children(): # Xóa các widget cũ
            widget.destroy()

        global entries
        entries = {}
        for idx, col in enumerate(columns): # Tạo các label và entry cho từng cột,enumerate trả về giá trị và chỉ số của phần tử
            label = tk.Label(input_frame, text=col, font=('Helvetica', 10, 'bold'), fg="#333333", bg="#d9f2e6") 
            label.grid(row=idx, column=0, sticky='w', padx=10, pady=8)

            entry = ttk.Entry(input_frame, width=50)
            entry.grid(row=idx, column=1, padx=10, pady=8)

            if col == "Car_id":
                entry.bind("<KeyRelease>", check_id_on_entry)
                global id_warning_label
                id_warning_label = tk.Label(input_frame, text="", font=('Helvetica', 9), fg="red", bg="#d9f2e6")
                id_warning_label.grid(row=idx, column=2, padx=10, pady=8)

            entries[col] = entry

        save_button = tk.Button(input_frame, text="Save", command=save_and_view_data, bg="#007bff", fg="white", font=('Helvetica', 10, 'bold'), bd=0, padx=20, pady=5)
        save_button.grid(row=len(columns), column=0, columnspan=2, pady=10)

    def check_id_on_entry(event):
        car_id = entries["Car_id"].get()
        if check_car_exists(car_id, car_data=car_data):
            id_warning_label.config(text="ID đã tồn tại.", fg="red")
        else:
            id_warning_label.config(text="")

    def save_and_view_data():
        car_id = entries["Car_id"].get()
        if check_car_exists(car_id, car_data=car_data):
            messagebox.showerror("Lỗi", "ID xe đã tồn tại. Vui lòng nhập ID khác")
            entries["Car_id"].delete(0, tk.END)
            entries["Car_id"].focus_set()  # đặt con trỏ lại phần car_id cho người dùng nhập lại
        else:
            if add_car(columns, entries, car_data, tree, input_frame, table_frame):
                input_frame.pack_forget()
                table_frame.pack(fill="both", expand=True)
                update_pagination(tree, car_data, pagination_frame, 0)

    def quit_app():
        root.quit()

    root = tk.Tk()
    root.title("Car Management System")
    root.geometry("1500x800")
    root.configure(bg="#e6f7ff")

    sidebar = tk.Frame(root, bg="#d9f2e6", width=100, height=700)
    sidebar.pack(side="left", fill="y")

    def create_logo():
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(script_dir, "logo.png")
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((80, 80), Image.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(sidebar, image=logo_photo, bg="#d9f2e6")
            logo_label.image = logo_photo
            logo_label.grid(row=0, column=0, padx=10, pady=10)
        except FileNotFoundError:
            messagebox.showerror("Error", "Logo file 'logo.png' not found.")
    create_logo()

    def create_nav_button(text, row, command=None):
        btn = tk.Button(sidebar, text=text, font=("Helvetica", 10, "bold"), fg="white", bg="#007bff", bd=0, padx=10, pady=10, command=command)
        btn.grid(row=row, column=0, sticky="ew", padx=10, pady=10)

    create_nav_button("📂 Load Data", 1, lambda: [load_data_from_csv(car_data, tree, input_frame, table_frame), update_pagination(tree, car_data, pagination_frame, 0)])
    create_nav_button("➕ Add Car", 2, open_input_window)
    create_nav_button("🖉 Update Car", 3, lambda: update_car_by_id(root, car_data, table_frame, input_frame, columns, tree))
    create_nav_button("🗑 Delete Car", 4, lambda: delete_car(columns, car_data, tree))
    create_nav_button("📊 Show Chart", 5, show_chart)
    create_nav_button("🚪 Quit", 6, quit_app)

    main_frame = tk.Frame(root, bg="#e6f7ff", padx=20, pady=20)
    main_frame.pack(side="right", fill="both", expand=True)

    title_label = tk.Label(main_frame, text="CAR MANAGEMENT APP", font=("Helvetica", 24, 'bold'), bg="#e6f7ff", fg="green")
    title_label.pack()

    input_frame = tk.Frame(main_frame, bg="#d9f2e6", padx=20, pady=20, bd=2, relief="groove")
    input_frame.pack_forget()

    search_frame = tk.Frame(main_frame, bg="#e6f7ff", pady=10)
    search_frame.pack(fill="x", pady=10)

    search_label = tk.Label(search_frame, text="Search by Company:", font=("Helvetica", 10, "bold"), bg="#e6f7ff")
    search_label.pack(side="left", padx=10)

    search_entry = ttk.Entry(search_frame, width=30)
    search_entry.pack(side="left", padx=10)

    search_button = tk.Button(search_frame, text="Search", bg="#007bff", fg="white", font=('Helvetica', 10, 'bold'), bd=0,
                              command=lambda: search_by_company(search_entry, columns, car_data, tree, pagination_frame))
    search_button.pack(side="left", padx=10)

    table_frame = tk.Frame(main_frame, bg="#d9f2e6", bd=2, relief="groove")
    table_frame.pack(fill="both", expand=True)

    

    pagination_frame = tk.Frame(main_frame, bg="#e6f7ff", pady=10)
    pagination_frame.pack(fill="x", pady=10)

    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col, command=lambda _col=col: sort_column(_col, columns, sort_states, car_data, tree))
        tree.column(col, anchor="center", width=120)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    load_data_from_csv(car_data, tree, input_frame, table_frame)
    update_pagination(tree, car_data, pagination_frame, 0)

    root.mainloop()
