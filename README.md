# Smart Movie Recommender System

The **Smart Movie Recommender System** is an end-to-end AI/ML based web application designed with a **Premium Dark UI**. It recommends similar movies to users based on their preferences using Content-Based Filtering techniques.

The project involves parsing a public movie dataset (TMDB), extracting rich text features (overview, genres, keywords, cast, crew) using NLP, and computing movie similarity via Cosine Similarity. The final model is deployed on a sleek Streamlit web interface that features a minimalist design, custom styling, and interactive elements.

## ✨ Features

*   **Smart Recommendations**: tailored movie suggestions using Cosine Similarity.
*   **Advanced Filtering & Sorting**:
    *   **Filter by Genre**: Narrow down recommendations to specific genres (e.g., Action, Drama).
    *   **Sort by Match Confidence**: See the most mathematically similar movies first.
    *   **Sort by High Rating**: Prioritize critically acclaimed movies.
    *   **Sort by Newest Release**: Discover the latest films similar to your taste.
*   **Premium Dark UI**: A professional dark theme with vibrant accents and minimalist design.
*   **Rich Movie Data**:
    *   **Live Posters**: High-quality movie posters fetched from TMDB.
    *   **Cast Info**: See top actors/actresses for every recommendation.
    *   **Ratings**: View the IMDB/TMDB rating for each film.

## 🛠 Tech Stack

*   **Python**: Core logic.
*   **Pandas & NumPy**: Data manipulation.
*   **Scikit-Learn**: Vectorization and Similarity computation.
*   **Streamlit**: Web framework (with custom CSS injection).
*   **TMDB API**: Movie assets (Posters, Cast, Ratings).

## 🚀 Setup & Installation

1.  **Clone the repository** (if applicable) or download the files.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: This project requires standard libraries like `pandas`, `scikit-learn`, `nltk`, `streamlit`, `requests`)*

3.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure

*   `app.py`: The main Streamlit application with custom UI logic and API integration.
*   `recommender.py`: Core logic for data finding, processing, and generating the similarity model.
*   `data/` or `*.csv`: Contains the TMDB dataset (`tmdb_5000_movies.csv`).
*   `requirements.txt`: Python dependencies.
*   `Project_Report.md`: Detailed report of the project architecture and features.

## 👥 Usage

*   Launch the app.
*   **Select a Movie**: Choose a reference movie from the dropdown menu (e.g., "Avatar").
*   **Apply Filters (Optional)**:
    *   **Genre**: Select a specific genre (e.g., Action, Comedy) to narrow down results.
*   **Choose Sorting Preference**:
    *   **Match Confidence**: Best mathematical match.
    *   **High Rating**: Top-rated movies.
    *   **Newest Release**: Most recent movies.
*   Click **"Find Similar Movies"**.
*   Enjoy the curated list of similar movies displayed with their official posters, ratings, and cast names.
