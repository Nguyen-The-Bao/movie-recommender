import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

conn = sqlite3.connect('data/movie.db')
movies = pd.read_sql_query("SELECT * FROM movies", conn)
ratings = pd.read_sql_query("SELECT * FROM ratings", conn)
conn.close()

# Tạo ma trận User-Item: hàng là phim, cột là user, giá trị là rating
movie_user_matrix = ratings.pivot_table(index='movieId', columns='userId', values='rating').fillna(0)

# Tính độ tương đồng giữa các phim (Item-based)
similarity_matrix = cosine_similarity(movie_user_matrix)
similarity_df = pd.DataFrame(similarity_matrix, index=movie_user_matrix.index, columns=movie_user_matrix.index)


def get_movie_title(movie_id):
    result = movies[movies['movieId'] == movie_id]['title'].values
    return result[0] if len(result) > 0 else "Không rõ"


def recommend_movies(movie_id, top_n=5):
    if movie_id not in similarity_df.index:
        return []
    similar_scores = similarity_df[movie_id].sort_values(ascending=False)
    similar_scores = similar_scores.drop(movie_id)  # bỏ chính nó ra
    top_similar = similar_scores.head(top_n)

    results = []
    for mid, score in top_similar.items():
        results.append({
            "movieId": int(mid),
            "title": get_movie_title(mid),
            "similarity": round(float(score), 3)
        })
    return results


# Test thử: gợi ý phim tương tự phim có movieId = 1 (Toy Story)
if __name__ == "__main__":
    test_movie_id = 1
    print(f"Phim gốc: {get_movie_title(test_movie_id)}\n")
    print("Các phim được gợi ý:")
    for movie in recommend_movies(test_movie_id):
        print(f"- {movie['title']} (độ tương đồng: {movie['similarity']})")