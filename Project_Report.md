# Project Report: Smart Movie Recommender System

## 1. Acknowledgement
I would like to express my gratitude to the open-source community for providing excellent libraries like Scikit-learn, Pandas, and Streamlit, which made this project possible. I also thank The Movie Database (TMDB) for providing the rich dataset used for this recommendation engine. Special thanks to my mentors/teachers for their guidance in understanding Machine Learning concepts.

## 2. Objective and Scope
*   **Objective**: To build a Content-Based Movie Recommendation System that suggests movies similar to a user’s choice based on textual metadata (plot, genre, cast).
*   **Scope**:
    *   The system is designed for English-language movies using the TMDB 5000 dataset.
    *   It uses a web-based interface (Streamlit) for easy user interaction.
    *   It focuses on similarity based on content (plot/cast/genre) rather than user collaborative history (ratings/behavior).

## 3. Problem Statement
In the digital age, users are overwhelmed by the vast amount of content available on streaming platforms (Netflix, Prime, etc.). "Choice Paralysis" is a common issue where users spend more time searching for a movie than watching one. There is a need for an intelligent system that filters this vast library and presents personalized suggestions based on a movie a user already likes.

## 4. Existing Approaches
*   **Popularity-Based Filtering**: Suggesting trending movies to everyone. (Problem: Not personalized).
*   **Collaborative Filtering**: Suggesting based on what other similar users liked. (Problem: "Cold Start" problem – requires a lot of user history data).
*   **Hybrid Systems**: Combining both. (Complex to implement for a standalone project).

## 5. Approach / Methodology - Tools and Technologies used
We adopted a **Content-Based Filtering** approach. This method recommends items similar to those a user liked in the past using item attributes.

**Tools & Tech Stack:**
*   **Python**: Primary programming language.
*   **Pandas & NumPy**: For data manipulation and vector handling.
*   **Scikit-Learn**: specifically `CountVectorizer` and `CosineSimilarity` for the mathematical engine.
*   **NLTK (Natural Language Toolkit)**: For text processing (stemming, removing stop words).
*   **Streamlit**: For creating the responsive web application frontend.
*   **TMDB API**: To fetch real-time movie posters and cast details.

## 6. Workflow
1.  **Data Collection**: Loading `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`.
2.  **Preprocessing**: Merging datasets, selecting features (genres, keywords, overview, cast), and cleaning text (removing spaces, lowercase).
3.  **Vectorization**: Converting the combined text tags into numerical vectors using `CountVectorizer`/`TfidfVectorizer`.
4.  **Similarity Calculation**: Computing a Cosine Similarity matrix (distance between vectors).
5.  **Recommendation Logic**: Sorting movies based on similarity scores.
6.  **Frontend Display**: Showing results with Posters and Metadata via Streamlit.

## 7. Assumptions
*   Users prefer movies that are textually similar (e.g., similar plot or same actors).
*   The TMDB dataset represents a sufficient variety of movies.
*   The user has an active internet connection (for fetching posters via API).

## 8. Implementation
The core logic resides in `recommender.py`:
*   **Data Cleaning**: Helper functions parse JSON columns (like 'genres') into string lists.
*   **Tag Creation**: A 'tags' column is created by combining Overview + Genres + Keywords + Top 3 Actors + Director.
*   **Stemming**: Words are reduced to their root form (e.g., "acting" -> "act") to improve match accuracy.
*   **Matrices**: A 5000x5000 similarity matrix is pre-computed.

The UI logic resides in `app.py`:
*   Captures user input.
*   Fetches dynamic data from TMDB API using the movie ID.
*   Renders the layout with custom CSS for a "Dark Premium" look.

## 9. Solution Design
The solution follows a Model-View-Controller (MVC) like pattern:
*   **Model**: The pre-computed Similarity Matrix and DataFrames.
*   **View**: Streamlit frontend displaying grids and cards.
*   **Controller**: Python logic mapping user selection to the recommendation function.

## 10. Challenges & Opportunities
*   **Challenges**:
    *   **Data Quality**: Handling missing posters or null values in the dataset.
    *   **API Limits**: Ensuring the app handles API keys gracefull without crashing.
    *   **Performance**: Calculating similarity for 5000 movies in real-time can be slow; optimized by pre-calculating or caching.
*   **Opportunities**:
    *   Implementing Hybrid Filtering (combining user ratings).
    *   Deploying to a public cloud (Heroku/AWS/Streamlit Cloud).

## 11. Reflections on the project
Building this project provided deep insights into NLP (Natural Language Processing) and Vector Space Models. It bridged the gap between raw data analysis and a user-facing product. Understanding the importance of UI/UX (adding posters/ratings) turned a simple script into a usable product.

## 12. Recommendations
*   For future iterations, use a larger dataset (like IMDB 1M) for better variety.
*   Implement "mood-based" filtering using sentiment analysis of the overview.

## 13. Outcome / Conclusion
The project successfully meets its objective. It accurately recommends movies sharing similar themes, actors, or genres. The "Dark UI" is responsive and mimics professional streaming platforms, providing a seamless user experience.

## 14. Enhancement Scope
*   **Personalized User Login**: Tracking user history.
*   **Search by Actor**: Allowing users to search "Tom Cruise" instead of just movie titles.
*   **Trailers**: Embedding YouTube trailers in the recommendation cards.

## 15. Research questions and responses
*   *Q: Why Cosine Similarity over Euclidean Distance?*
    *   A: In text analysis, the magnitude of vectors (length of document) matters less than the angle (content overlap). Cosine similarity captures the orientation (similarity) better for high-dimensional text data.
*   *Q: How to handle the Cold Start problem?*
    *   A: Content-based filtering (our approach) naturally solves the cold start problem for *new items* as long as they have metadata, unlike collaborative filtering which needs user interaction.

## 16. References
1.  **Dataset**: [Kaggle TMDB 5000 Movie Dataset](https://www.kaggle.com/tmdb/tmdb-movie-metadata)
2.  **Libraries**: [Scikit-learn Documentation](https://scikit-learn.org/), [Streamlit Docs](https://docs.streamlit.io/)
3.  **Concepts**: "Recommender Systems: The Textbook" by Charu C. Aggarwal.

## 17. Link to code and executable file
*   **GitHub Repository**: [https://github.com/vandana206/Movie_Recommendation-_system](https://github.com/vandana206/Movie_Recommendation-_system)
*   **Main Executable**: `app.py`
