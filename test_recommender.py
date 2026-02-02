import recommender
import time

print("Loading and processing data...")
start = time.time()
df = recommender.load_data()
df = recommender.prepare_data(df)
print(f"Data processed in {time.time() - start:.2f} seconds.")

print("Building similarity matrix...")
start = time.time()
sim_matrix = recommender.build_similarity_matrix(df)
print(f"Matrix built in {time.time() - start:.2f} seconds.")

test_movie = "Avatar"
print(f"Recommendations for {test_movie}:")
recs = recommender.get_recommendations(test_movie, df, sim_matrix)
for movie in recs:
    print(f"- {movie}")
