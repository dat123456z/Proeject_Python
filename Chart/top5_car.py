import pandas as pd
data = pd.read_csv("data.csv")
# Tạo DataFrame chứa 5 loại xe bán chạy nhất cùng với số lượng
top_5_models_df = data['Model'].value_counts().head(5).reset_index()
top_5_models_df.columns = ['Model', 'Number of Sales']

print("Top 5 Best-Selling Car Models:")
print(top_5_models_df)
