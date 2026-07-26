import sqlite3
import pandas as pd

conn = sqlite3.connect('data/movie.db')

# Thử query 5 dòng đầu bảng movies
df = pd.read_sql_query("SELECT * FROM movies LIMIT 5", conn)
print(df)

conn.close()