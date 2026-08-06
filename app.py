from flask import Flask, render_template, request, jsonify
import pandas as pd
import sqlite3
from hybrid import recommend_smart, get_movie_title

app = Flask(__name__)

# Load danh sách phim để hiển thị dropdown
conn = sqlite3.connect('data/movie.db', check_same_thread=False)
movies = pd.read_sql_query("SELECT * FROM movies", conn)
conn.close()

@app.route('/')
def home():
    movie_list = movies.head(50)[['movieId', 'title']].to_dict('records')
    return render_template('index.html', movies=movie_list)

@app.route('/api/recommend')
def api_recommend():
    movie_id = int(request.args.get('movie_id'))
    original_title = get_movie_title(movie_id)
    results = recommend_smart(movie_id)
    return jsonify({"original": original_title, "recommendations": results})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)