import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity

conn = sqlite3.connect('data/movie.db')
ratings = pd.read_sql_query("SELECT * FROM ratings", conn)
conn.close()

# Chia dữ liệu train/test
train, test = train_test_split(ratings, test_size=0.2, random_state=42)

# Ma trận từ tập train
train_matrix = train.pivot_table(index='movieId', columns='userId', values='rating').fillna(0)
similarity = cosine_similarity(train_matrix)
similarity_df = pd.DataFrame(similarity, index=train_matrix.index, columns=train_matrix.index)


def predict_rating(user_id, movie_id):
    if movie_id not in similarity_df.index or user_id not in train_matrix.columns:
        return train['rating'].mean()  # fallback: điểm trung bình

    sim_scores = similarity_df[movie_id]
    user_ratings = train_matrix[user_id]

    rated_mask = user_ratings > 0
    if rated_mask.sum() == 0:
        return train['rating'].mean()

    weighted_sum = (sim_scores[rated_mask] * user_ratings[rated_mask]).sum()
    sim_sum = sim_scores[rated_mask].sum()

    if sim_sum == 0:
        return train['rating'].mean()
    return weighted_sum / sim_sum


# Tính RMSE trên tập test (lấy mẫu 200 dòng cho nhanh)
sample_test = test.sample(min(200, len(test)), random_state=42)
predictions = []
actuals = []

for _, row in sample_test.iterrows():
    pred = predict_rating(row['userId'], row['movieId'])
    predictions.append(pred)
    actuals.append(row['rating'])

rmse = np.sqrt(np.mean((np.array(predictions) - np.array(actuals)) ** 2))
print(f"RMSE: {rmse:.4f}")