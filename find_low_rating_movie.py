import sqlite3
import pandas as pd

conn = sqlite3.connect('data/movie.db')
ratings_count = pd.read_sql_query(
    "SELECT movieId, COUNT(*) as num_ratings FROM ratings GROUP BY movieId ORDER BY num_ratings ASC LIMIT 10", conn
)
movies = pd.read_sql_query("SELECT * FROM movies", conn)
conn.close()

result = ratings_count.merge(movies, on='movieId')
print(result[['movieId', 'title', 'num_ratings']])