# Project Report: Smart Movie Recommender System

## 1. Introduction
The Smart Movie Recommender System is a machine learning-based web application that suggests movies similar to a user's selection. Utilizing Content-Based Filtering, the system analyzes movie metadata such as genres, keywords, overview, and cast information to identify and rank similarities.

## 2. Problem Statement
With the abundance of movie content available online, users often struggle to decide what to watch next. A recommendation system solves this by filtering information and predicting items that a user would likely prefer.

## 3. Methodology
### 3.1 Data Collection
The system uses the TMDB 5000 Movie Dataset, which includes high-quality metadata for thousands of films.

### 3.2 Data Preprocessing
*   **Text Cleaning**: Removal of stop words, lowercasing, and lemmatization using the NLTK library.
*   **Feature Engineering**: Extraction of genres and keywords from JSON formats into string tags.
*   **Vectorization**: The `TfidfVectorizer` (Term Frequency-Inverse Document Frequency) is used to convert text data into numerical vectors, representing the importance of words in the dataset.

### 3.3 Similarity Calculation
*   **Cosine Similarity**: Measures the cosine of the angle between two non-zero vectors. This metric is used to determine how similar two movies are based on their vectorized features.

## 4. System Architecture
### 4.1 Backend (Python)
*   **`recommender.py`**: Handles data loading, cleaning, and model generation.
*   **`app.py`**: Orchestrates the application logic, calling the recommender functions and handling the API requests for posters.

### 4.2 Frontend (Streamlit)
The application offers a rich interactive experience with the following controls:

1.  **Movie Selection**: A searchable dropdown to pick the reference movie.
2.  **Genre Filter**: Allows users to restrict recommendations to a specific genre (derived from the dataset).
3.  **Sorting Mechanisms**:
    *   **Match Confidence**: Default sorting based on the cosine similarity score.
    *   **High Rating**: Re-ranks the top similar movies by their `vote_average`.
    *   **Newest Release**: Re-ranks movies by their `release_date`.

**Visual Output**:
*   **Dynamic Grids**: Movies are displayed in a responsive grid layout.
*   **Movie Cards**: Each card displays the Poster, Title, Cast, Rating, and Similarity Score.

## 5. Conclusion
The Smart Movie Recommender System successfully demonstrates the application of Natural Language Processing and Machine Learning in a user-friendly product. The integration of live API data ensures the content remains engaging and visually appealing.
