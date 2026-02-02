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
*   Provides a responsive, dark-themed UI.
*   Displays movie cards with:
    *   **Posters**: Fetched dynamically via API.
    *   **Cast**: Top actors involved in the movie.
    *   **Ratings**: Average viewer score.
    *   **Match %**: Visual indicator of similarity.

## 5. Conclusion
The Smart Movie Recommender System successfully demonstrates the application of Natural Language Processing and Machine Learning in a user-friendly product. The integration of live API data ensures the content remains engaging and visually appealing.
