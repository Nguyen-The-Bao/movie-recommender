import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('data/movie.db')

movies = pd.read_sql_query("SELECT * FROM movies", conn)
ratings = pd.read_sql_query("SELECT * FROM ratings", conn)

conn.close()

# 1. Thống kê cơ bản
print("Số lượng phim:", movies.shape[0])
print("Số lượng đánh giá:", ratings.shape[0])
print("Số lượng người dùng:", ratings['userId'].nunique())

# 2. Phân bố điểm rating
plt.figure(figsize=(6,4))
ratings['rating'].value_counts().sort_index().plot(kind='bar')
plt.title('Phân bố điểm rating')
plt.xlabel('Điểm rating')
plt.ylabel('Số lượng')
plt.tight_layout()
plt.savefig('data/phan_bo_rating.png')
plt.show()

# 3. Top 10 phim được đánh giá nhiều nhất
top_movies = ratings['movieId'].value_counts().head(10)
top_movies_info = movies[movies['movieId'].isin(top_movies.index)]
print("\nTop 10 phim được đánh giá nhiều nhất:")
print(top_movies_info[['title']])