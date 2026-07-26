from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load dữ liệu và tính toán 1 lần khi server khởi động
conn = sqlite3.connect('data/movie.db', check_same_thread=False)
movies = pd.read_sql_query("SELECT * FROM movies", conn)
ratings = pd.read_sql_query("SELECT * FROM ratings", conn)

movie_user_matrix = ratings.pivot_table(index='movieId', columns='userId', values='rating').fillna(0)
similarity_matrix = cosine_similarity(movie_user_matrix)
similarity_df = pd.DataFrame(similarity_matrix, index=movie_user_matrix.index, columns=movie_user_matrix.index)

def get_movie_title(movie_id):
    result = movies[movies['movieId'] == movie_id]['title'].values
    return result[0] if len(result) > 0 else "Không rõ"

def recommend_movies(movie_id, top_n=5):
    if movie_id not in similarity_df.index:
        return []
    similar_scores = similarity_df[movie_id].sort_values(ascending=False).drop(movie_id)
    top_similar = similar_scores.head(top_n)
    return [{"movieId": int(mid), "title": get_movie_title(mid), "similarity": round(float(score), 3)}
            for mid, score in top_similar.items()]

@app.route('/')
def home():
    # Lấy 20 phim đầu để hiển thị trong dropdown chọn
    movie_list = movies.head(50)[['movieId', 'title']].to_dict('records')
    return render_template('index.html', movies=movie_list)

@app.route('/api/recommend')
def api_recommend():
    movie_id = int(request.args.get('movie_id'))
    original_title = get_movie_title(movie_id)
    results = recommend_movies(movie_id)
    return jsonify({"original": original_title, "recommendations": results})

if __name__ == '__main__':
    app.run(debug=True)