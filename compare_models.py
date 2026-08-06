from recommend import recommend_movies, get_movie_title as get_title_collab
from content_based import recommend_by_content, get_movie_title as get_title_content

def compare(movie_id, top_n=5):
    title = get_title_collab(movie_id)
    print(f"= Phim gốc: {title} \n")

    print(" Collaborative Filtering (dựa trên rating) ")
    for m in recommend_movies(movie_id, top_n):
        print(f"- {m['title']} (similarity: {m['similarity']})")

    print("\n Content-based Filtering (dựa trên thể loại) ")
    for m in recommend_by_content(movie_id, top_n):
        print(f"- {m['title']} (similarity: {m['similarity']})")

if __name__ == "__main__":
    compare(1)  # Toy Story
    print("\n" + "="*50 + "\n")
    compare(50)  # thử thêm 1 phim khác, có thể đổi movieId