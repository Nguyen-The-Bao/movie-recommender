import sqlite3
import pandas as pd

# Kết nối (tự tạo file movie.db nếu chưa có)
conn = sqlite3.connect('data/movie.db')

# Đọc dữ liệu CSV
movies = pd.read_csv('data/movies.csv')
ratings = pd.read_csv('data/ratings.csv')

# Đưa dữ liệu vào CSDL (tạo bảng tự động theo tên cột)
movies.to_sql('movies', conn, if_exists='replace', index=False)
ratings.to_sql('ratings', conn, if_exists='replace', index=False)

conn.close()
print("Đã tạo CSDL thành công!")