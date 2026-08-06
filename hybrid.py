from recommend import similarity_df as collab_similarity, get_movie_title
from content_based import content_similarity_df
import sqlite3
import pandas as pd

def recommend_hybrid(movie_id, top_n=5, weight_collab=0.5, weight_content=0.5):
    if movie_id not in collab_similarity.index or movie_id not in content_similarity_df.index:
        return []

    collab_scores = collab_similarity[movie_id]
    content_scores = content_similarity_df[movie_id]

    # Cộng có trọng số 2 điểm số lại
    hybrid_scores = (weight_collab * collab_scores) + (weight_content * content_scores)
    hybrid_scores = hybrid_scores.drop(movie_id).sort_values(ascending=False)

    top_similar = hybrid_scores.head(top_n)
    return [{"movieId": int(mid), "title": get_movie_title(mid), "similarity": round(float(score), 3)}
            for mid, score in top_similar.items()]


conn = sqlite3.connect('data/movie.db')
ratings_count = pd.read_sql_query(
    "SELECT movieId, COUNT(*) as num_ratings FROM ratings GROUP BY movieId", conn
)
conn.close()

ratings_count_dict = dict(zip(ratings_count['movieId'], ratings_count['num_ratings']))


def recommend_smart(movie_id, top_n=5, min_ratings=5):
    num_ratings = ratings_count_dict.get(movie_id, 0)

    if num_ratings < min_ratings:
        print(f"[Phim có ít rating ({num_ratings}) → dùng Content-based]")
        from content_based import recommend_by_content
        return recommend_by_content(movie_id, top_n)
    else:
        print(f"[Phim có đủ rating ({num_ratings}) → dùng Hybrid]")
        return recommend_hybrid(movie_id, top_n)


if __name__ == "__main__":
    test_movie_id = 49
    print(f"Phim gốc: {get_movie_title(test_movie_id)}\n")
    for movie in recommend_smart(test_movie_id):
        print(f"- {movie['title']} (similarity: {movie['similarity']})")