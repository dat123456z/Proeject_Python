import pandas as pd
import os

# Đọc tệp CSV
file_path = 'D:\\Proeject_Python-main\\data\\raw\\data.csv'
data = pd.read_csv(file_path)  # Sử dụng dấu gạch chéo để tránh lỗi

# Chọn các cột cần thiết
selected_columns = ['Car_id', 'Date', 'Customer Name', 'Gender', 'Annual Income', 'Dealer_Name', 'Company', 'Model', 'Color', 'Price', 'Phone']
selected_data = data[selected_columns]

# 1. Loại bỏ các hàng có giá trị trống
selected_data = selected_data.dropna()

# 2. Chuẩn hóa các khoảng trắng và kiểm tra định dạng dữ liệu
selected_data = selected_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# 3. Chuẩn hóa định dạng cột 'Annual Income' và 'Price'
def clean_range(value):
    if isinstance(value, str):
        value = value.replace(',', '').strip()  # Loại bỏ dấu phẩy và khoảng trắng
        if '-' in value:  # Nếu có khoảng giá trị
            try:
                low, high = map(float, value.split('-'))
                return (low + high) / 2
            except ValueError:
                return None  # Đánh dấu giá trị không hợp lệ là None
        try:
            return float(value)  # Chuyển đổi thành float nếu là số
        except ValueError:
            return None  # Đánh dấu giá trị không hợp lệ là None
    return value

# Đảm bảo cột 'Annual Income' và 'Price' tồn tại
if 'Annual Income' in selected_data.columns:
    selected_data['Annual Income'] = selected_data['Annual Income'].apply(clean_range)
if 'Price' in selected_data.columns:
    selected_data['Price'] = selected_data['Price'].apply(clean_range)

# Loại bỏ các hàng có giá trị None sau khi xử lý
selected_data = selected_data.dropna()

# 4. Loại bỏ các hàng trùng lặp
selected_data = selected_data.drop_duplicates()

# Lưu DataFrame mới vào tệp CSV đã làm sạch
output_path = 'data/clean/Cleaned_Car_Dataset.csv'
directory = os.path.dirname(output_path)

# Tạo thư mục nếu chưa tồn tại
if not os.path.exists(directory):
    os.makedirs(directory)

# Lưu dữ liệu đã làm sạch
selected_data.to_csv(output_path, index=False)

print(f"Tệp đã được làm sạch và lưu tại: {output_path}")
