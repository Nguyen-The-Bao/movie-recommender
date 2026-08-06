import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

conn = sqlite3.connect('data/movie.db')
movies = pd.read_sql_query("SELECT * FROM movies", conn)
conn.close()

# Xử lý cột genres: thay dấu | thành khoảng trắng để TF-IDF hiểu là các từ riêng biệt
movies['genres_clean'] = movies['genres'].str.replace('|', ' ', regex=False)

# Chuyển thể loại phim thành vector số bằng TF-IDF
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(movies['genres_clean'])

# Tính độ tương đồng giữa các phim dựa trên thể loại
content_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
content_similarity_df = pd.DataFrame(content_similarity, index=movies['movieId'], columns=movies['movieId'])

def get_movie_title(movie_id):
    result = movies[movies['movieId'] == movie_id]['title'].values
    return result[0] if len(result) > 0 else "Không rõ"

def recommend_by_content(movie_id, top_n=5):
    if movie_id not in content_similarity_df.index:
        return []
    similar_scores = content_similarity_df[movie_id].sort_values(ascending=False).drop(movie_id)
    top_similar = similar_scores.head(top_n)
    return [{"movieId": int(mid), "title": get_movie_title(mid), "similarity": round(float(score), 3)}
            for mid, score in top_similar.items()]

# Test thử
if __name__ == "__main__":
    test_movie_id = 1
    print(f"Phim gốc: {get_movie_title(test_movie_id)}\n")
    print("Gợi ý theo Content-based (dựa trên thể loại):")
    for movie in recommend_by_content(test_movie_id):
        print(f"- {movie['title']} (độ tương đồng: {movie['similarity']})")