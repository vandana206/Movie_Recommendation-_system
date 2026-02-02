# Project Report: Smart Movie Recommender System

---

## 1. Acknowledgement

The successful completion of this project, the **Smart Movie Recommender System**, would not have been possible without the support and guidance of several individuals and resources.

First and foremost, I would like to express my sincere gratitude to my mentor/supervisor for their invaluable guidance, constructive feedback, and constant encouragement throughout the development of this project. Their insights into Machine Learning and Software Engineering principles were instrumental in shaping the architecture of this system.

I am also deeply indebted to the open-source community. This project stands on the shoulders of giants, specifically the developers and maintainers of:
*   **Python**: For providing a robust and versatile programming environment.
*   **Scikit-Learn**: For making complex machine learning algorithms accessible and easy to implement.
*   **Pandas and NumPy**: For their powerful data manipulation capabilities which formed the backbone of our data preprocessing pipeline.
*   **Streamlit**: For revolutionizing the way data scripts are turned into shareable web apps.

A special vote of thanks goes to **The Movie Database (TMDB)** for providing a rich, open-access dataset and a reliable API. The availability of high-quality metadata, including posters, cast details, and plot summaries, significantly enhanced the user experience of our application.

Finally, I would like to thank my friends and family for their patience and support during the long hours of coding and debugging required to bring this project to life.

---

## 2. Objective and Scope

### 2.1 Objective
The primary objective of this project is to design and develop a robust, user-friendly **Content-Based Movie Recommendation System**. The system aims to mitigate the problem of "Choice Overload" faced by users on modern streaming platforms by providing personalized movie suggestions.

Specific sub-objectives include:
*   To parse and process large-scale movie datasets (TMDB 5000) to extract meaningful features.
*   To implement Natural Language Processing (NLP) techniques to analyze text metrics (Plot, Keywords, Genres).
*   To utilize Vector Space Models and Cosine Similarity to mathematically quantify the relationship between different movies.
*   To deploy the model on a responsive, aesthetically pleasing web interface that allows users to interact with the system in real-time.

### 2.2 Scope
The scope of the project helps define the boundaries within which the system operates:

*   **Data Scope**: The system utilizes the TMDB 5000 Movies dataset. It focuses on English-language movies but includes metadata for international films present in the dataset. The recommendation engine is limited to the movies present in this static dataset, though metadata (posters) is fetched live.
*   **Functional Scope**:
    *   **Recommendation**: Suggest 5-10 similar movies based on a selected movie.
    *   **Filtering**: user capability to filter results by Genre.
    *   **Sorting**: Capability to sort results by Rating, Release Date, or Similarity Score.
    *   **Visualization**: Displaying posters, ratings, and cast information.
*   **Target Audience**: Movie enthusiasts, streaming platform users, and data science students interested in recommendation algorithms.
*   **Exclusions**: The system does NOT use Collaborative Filtering (User-Item interactions) due to the lack of user history data. It does not support user accounts/login or watch history tracking in this version.

---

## 3. Problem Statement

### 3.1 The "Choice Paradox"
In the current digital era, we are witnessing an explosion of content. Streaming giants like Netflix, Amazon Prime, and Disney+ host libraries containing thousands of titles. While this variety is a boon, it creates a psychological phenomenon known as the **"Paradox of Choice"**.

*   Users spend significantly more time *searching* for something to watch than actually *watching* it.
*   The overwhelming number of options leads to decision fatigue.
*   Users often end up watching content that doesn't align with their specific tastes because they cannot navigate the catalogue effectively.

### 3.2 The Need for Personalization
Generic lists like "Top 10 Trending" are insufficient because they do not account for individual preferences. A user who enjoys "Inception" (Sci-Fi/Thriller) is unlikely to be interested in a generic "Top Trending" Romantic Comedy.

### 3.3 The Solution
There is a critical need for an intelligent system that acts as a personalized curator. By analyzing the *attributes* of a movie a user already likes (e.g., "I like movies with Tom Cruise usually involving spies"), the system can intelligently surface other movies that share those attributes, thereby saving time and enhancing satisfaction.

---

## 4. Existing Approaches

To solve the recommendation problem, three primary approaches exist in the industry. We analyzed these before selecting our methodology.

### 4.1 Popularity-Based Filtering
*   **Concept**: Recommend items that are currently trending or have the highest global ratings.
*   **Mechanism**: Sort the entire movies database by `vote_average` or `popularity` score and return the top N.
*   **Pros**: Extremely easy to implement; solves the "Cold Start" problem for new users.
*   **Cons**: Not personalized. Every user sees the exact same list. It fails to capture unique or niche tastes.

### 4.2 Collaborative Filtering
*   **Concept**: "Users who liked this also liked that." It relies on past user behavior (ratings, clicks, watch history).
*   **Mechanism**: Uses Matrix Factorization (SVD) or Neural Networks to predict a user's rating for an unseen movie based on similar users.
*   **Pros**: Highly accurate; capable of discovering latent interests (serendipity).
*   **Cons**:
    *   **Cold Start Problem**: Cannot recommend to a new user with no history.
    *   **Sparsity**: Requires a massive amount of data to be effective (millions of ratings).
    *   **Scalability**: Computationally expensive to update as users grow.

### 4.3 Content-Based Filtering (Selected Approach)
*   **Concept**: Recommend items similar to those a user liked based on item attributes (content).
*   **Mechanism**: Analyze metadata (Director, Actors, Plot keywords). If a user likes Movie A, and Movie B has the same Director and similar plot keywords, recommend Movie B.
*   **Pros**:
    *   **No User Data Needed**: Works immediately for any user without needing their history.
    *   **Transparent**: We can explain *why* a movie was recommended (e.g., "Because it is also a Sci-Fi movie directed by Christopher Nolan").
*   **Cons**:
    *   **Overspecialization**: Tends to recommend more of the same (e.g., only recommends Action movies if user selects Action).
    *   **Data Dependency**: Only as good as the metadata available.

**Conclusion**: We chose **Content-Based Filtering** for this project because it is feasible without a massive user base and allows us to demonstrate NLP and Vector Space techniques effectively.

---

## 5. Approach / Methodology - Tools and Technologies

Our methodology involves treating Movie Recommendation as a **Text Similarity Problem**. By converting the textual description of movies into mathematical vectors, we can calculate the distance between them. The closer the vectors, the more similar the movies.

### 5.1 Tools and Technologies

#### **1. Python (Language)**
Python was chosen for its dominance in Data Science. Its rich ecosystem of libraries allows for rapid prototyping and robust deployment.

#### **2. Pandas (Data Manipulation)**
Used for:
*   Loading CSV datasets.
*   Handling missing values (Imputation).
*   Merging multiple datasets (merging 'credits' with 'movies' on `id`).
*   Data transformation (converting stringified JSON columns into Python lists).

#### **3. Scikit-Learn (Machine Learning)**
The core engine of the project.
*   `CountVectorizer`: We used this to convert the text 'tags' into a Token Count Matrix. We chose CountVectorizer over TfidfVectorizer because, in our specific use case (keywords and cast names), the *frequency* of a word matters less than its *presence*. Also, common names (like "James" in a character name) shouldn't be penalized heavily as they might be key connectors.
*   `cosine_similarity`: Used to calculate the angular distance between movie vectors. Values range from 0 (completely different) to 1 (identical).

#### **4. NLTK (Natural Language Toolkit)**
Used for **PorterStemmer**. Stemming is critical to reduce the dimensionality of our vector space.
*   *Before Stemming*: "Acting", "Acts", "Actor" are treated as 3 different words.
*   *After Stemming*: All become "act".
This ensures that "love" and "loving" match in the plot descriptions.

#### **5. Streamlit (Frontend)**
Streamlit allowed us to build a full-stack web application completely in Python.
*   **Session State**: Used to cache heavy data (Similarity Matrix) so it doesn't reload on every interaction.
*   **Layouts**: `st.columns` used to create the grid view for posters.

#### **6. TMDB API (Data Enrichment)**
While our algorithm runs on the local CSV dataset, we rely on the TMDB API to make the app visually appealing.
*   **Endpoint**: `GET /movie/{movie_id}`
*   **Data Retrieved**: High-resolution Poster Path (`.jpg`), Cast Images (for future scope), and updated Ratings.

---

## 6. Workflow

The project lifecycle followed a structured data science pipeline:

### Phase 1: Data Acquisition
*   Downloaded `tmdb_5000_movies.csv` (contains Title, Overview, Genres, Keywords).
*   Downloaded `tmdb_5000_credits.csv` (contains Cast, Crew).
*   Verified data integrity and checked for corruption.

### Phase 2: Data Preprocessing (Crucial Step)
1.  **Merging**: Combined the two CSVs into a single DataFrame using `title` or `id` as the key.
2.  **Feature Selection**: Discarded irrelevant columns like `budget`, `homepage`, `runtime` as they don't contribute significantly to content similarity. Kept: `movie_id`, `title`, `overview`, `genres`, `keywords`, `cast`, `crew`.
3.  **JSON Parsing**: Columns like `genres` were stored as stringified JSON (e.g., `"[{"id": 28, "name": "Action"}]"`). We wrote a helper function to extract just the names (e.g., `['Action']`).
4.  **Handling Cast/Crew**: Extracted only the **Top 3 Actors** and the **Director**.
5.  **Text Cleaning**:
    *   Removed spaces between names (e.g., "Tom Cruise" -> "TomCruise"). This is vital so the logic doesn't confuse "Tom Cruise" with "Tom Hanks" because of the common word "Tom".
    *   Converted everything to lowercase.
    *   Tokenized the `overview` into list of words.

### Phase 3: Tag Generation
*   Concatenated all processed features into a single column called `tags`.
*   Example Tag: *"in the 22nd century a paraplegic marine... samworthington zoesaldana action scifi cultureclash future space war"*

### Phase 4: Vectorization & Similarity
1.  **Vectorization**: Initialized `CountVectorizer` with `max_features=5000` (focusing on top 5000 most frequent words) and `stop_words='english'`.
2.  **Transformation**: Transformed the 5000 movies into a `5000x5000` sparse matrix.
3.  **Similarity**: Calculated the Dot Product of the matrix with itself (Cosine Similarity). Result is a lookup table where `matrix[i][j]` represents the similarity between Movie `i` and Movie `j`.

---

## 7. Assumptions

In designing this system, the following assumptions were made:

1.  **Metadata Sufficiency**: We assume that the plot summary (`overview`) and keywords accurately describe the movie's essence.
2.  **Attribute Equality**: We weigh all words equally initially. The word "Love" in the plot is considered as important as "Action" in the genre.
3.  **Single User Session**: The app currently runs as a single-session instance without persistent user profiles.
4.  **Language**: The model assumes English is the primary language for textual analysis.
5.  **API Availability**: The application assumes the TMDB API service is online and the provided API key is valid for fetching images.

---

## 8. Implementation

### 8.1 Core Recommendation Logic (`recommender.py`)
The heavy lifting is done here. The script handles the loading of the CSVs and the pre-computed similarity matrix.

```python
def get_recommendations(movie_title, df, cosine_sim):
    # 1. Find the index of the movie in the dataframe
    idx = df[df['title'] == movie_title].index[0]
    
    # 2. Get similarity scores for this movie (array of 5000 floats)
    distances = cosine_sim[idx]
    
    # 3. Create pairs of (index, score) and sort them descending
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    
    # 4. Return top 30 candidates for further filtering
    return [df.iloc[u[0]] for u in movie_list[1:31]]
```

### 8.2 User Interface Logic (`app.py`)
Streamlit manages the frontend state.
*   **State Management**: `st.session_state` is used to store the `tmdb_api_key` and cached API responses. This prevents the app from making redundant network requests when the user changes a filter (like "Genre").
*   **Error Handling**: The `get_poster_url` function includes `try-except` blocks to handle connection timeouts or invalid API keys gracefully, returning a placeholder or `None` instead of crashing the app.

---

## 9. Solution Design

### 9.1 System Architecture
The High-Level Design (HLD) of the system can be visualized as three distinct layers:

1.  **Data Layer**:
    *   **Static Data**: CSV Files (`tmdb_5000_movies.csv`) stored locally in `data/` folder.
    *   **Dynamic Data**: Poster images and Cast details fetched over HTTPS from `api.themoviedb.org`.
2.  **Processing Layer (Logic)**:
    *   **Vector Space Model**: The in-memory representation of movies as vectors.
    *   **Filtering Engine**: Python logic that applies Genre and Sort filters on top of the raw similarity results.
3.  **Presentation Layer (UI)**:
    *   **Streamlit Server**: Renders HTML/CSS.
    *   **Custom CSS**: Injected into the page to override default styles for a "Dark Mode" aesthetic.

### 9.2 Data Flow
1.  User selects "Avatar".
2.  App looks up ID for "Avatar".
3.  App queries Similarity Matrix -> Returns `[Movie_B, Movie_C, Movie_D]`.
4.  App applies User Filters (e.g., "Only Action").
5.  App calls `get_poster_url(ID)` for the filtered list.
6.  App renders the Grid View with images and titles.

---

## 10. Challenges & Opportunities

### 10.1 Key Challenges Faced
1.  **The "Curse of Dimensionality"**:
    *   Initially, our vocabulary size was massive (30,000+ words). This made the vector computation slow and prone to noise.
    *   *Solution*: We used Stemming (NLTK) and limited `max_features` to 5000.
2.  **Data Quality Issues**:
    *   Many movies had missing overviews or malformed dates.
    *   *Solution*: Implemented robust data cleaning steps in `load_data` to fill `NaN` with empty strings or defaults.
3.  **API Latency**:
    *   Fetching posters for 10 movies sequentially took 5-6 seconds, which is bad UX.
    *   *Solution*: Implemented caching (`@st.cache_data`) and optimized the request loops.
4.  **Duplicate Entries**:
    *   The dataset contained duplicate movie titles.
    *   *Solution*: We dropped duplicates during the preprocessing stage based on `title`.

---

## 11. Reflections on the project

Undertaking this project was a significant learning curve. It reinforced the understanding that **Data Cleaning is 80% of Machine Learning**. The algorithm itself (Cosine Similarity) is mathematically straightforward, but its effectiveness depends entirely on how well we engineer the tags.

Key Takeaways:
1.  **Feature Engineering is King**: Merging the Director's name with the plot summary significantly improved recommendation quality compared to using just the plot.
2.  **User Experience Matters**: A great algorithm with a poor UI is useless. Adding the posters and "Dark Mode" transformed the project from a script into a product.
3.  **Optimization**: Handling large matrices in memory requires awareness of data types and efficiency.

---

## 12. Recommendations

Based on the development experience, I recommend the following for similar future projects:
1.  **Use Hybrid Models**: If user data is available, always combine Content-Based with Collaborative Filtering to solve the "Overspecialization" issue.
2.  **Cloud Decomposition**: For larger datasets (100k+ movies), standard Cosine Similarity matrices (O(N^2)) become too large for RAM. Use **Approximate Nearest Neighbors (ANN)** algorithms like Spotify's **Annoy** or Facebook's **Faiss**.
3.  **Mobile First**: Design the UI to be mobile-responsive from Day 1.

---

## 13. Outcome / Conclusion

The **Smart Movie Recommender System** was successfully developed and deployed.

**Success Metrics**:
*   **Accuracy**: Qualitative testing shows high relevance. E.g., Selecting "The Dark Knight" correctly recommends "Batman Begins", "The Dark Knight Rises", and other crime thrillers.
*   **Performance**: Recommendations are generated in < 200ms.
*   **Usability**: The app handles edge cases (missing posters) without breaking.

In conclusion, the project successfully demonstrates the power of Content-Based Filtering using NLP. It is a functional, visually appealing tool that solves the "Choice Paradox" effectively for its defined scope.

---

## 14. Enhancement Scope

The project has immense potential for future enhancements:

1.  **Deep Learning Integration**:
    *   Use **Word2Vec** or **BERT** embeddings instead of simple CountVectorizer to capture semantic meaning (e.g., understanding that "King" and "Queen" are related).
2.  **Sentiment Analysis**:
    *   Analyze user reviews to understand if a movie is "Feel Good" or "Depressing" and allow users to filter by Mood.
3.  **User Profiles**:
    *   Add "Login" functionality using Firebase or SQL.
    *   Allow users to "Like" movies to build a personal profile vector.
4.  **Voice Search**:
    *   Integrate a voice-to-text library to allow users to search for movies vocally.

---

## 15. Research Questions and Responses

### Q1: Why use Cosine Similarity instead of Euclidean Distance?
**Response**: In high-dimensional text data, the *magnitude* of the vector often represents the length of the document (word count), which is irrelevant for similarity. We care about the *orientation* (overlap of topics). Cosine similarity measures the angle, making it length-invariant and ideal for text classification.

### Q2: How does the system handle names like "Leonardo DiCaprio"?
**Response**: We used a preprocessing step to remove spaces, converting it to "LeonardoDiCaprio". This treats the full name as a single unique token. Without this, the system might match "Leonardo Da Vinci" with "Leonardo DiCaprio" simply because of the common token "Leonardo", which would be incorrect contextually.

### Q3: What is the impact of removing Stop Words?
**Response**: Stop words (like "the", "is", "items") appear frequently but carry little semantic meaning. Removing them reduces the noise in our vector space, ensuring that matches are based on meaningful keywords (like "Alien", "Space", "War") rather than grammar.

### Q4: Can this system scale to 1 Million movies?
**Response**: As is, no. A 1M x 1M matrix would require Terabytes of RAM. For scale, we would need to switch to **Approximate Nearest Neighbors (ANN)** techniques or an inverted index (like Elasticsearch).

---

## 16. References

1.  **Dataset Source**:
    *   *Kaggle TMDB 5000 Movie Dataset*: [https://www.kaggle.com/tmdb/tmdb-movie-metadata](https://www.kaggle.com/tmdb/tmdb-movie-metadata)
2.  **Academic Resources**:
    *   *Aggarwal, C. C. (2016). Recommender Systems: The Textbook. Springer.*
    *   *Manning, C. D., Raghavan, P., & Schütze, H. (2008). Introduction to Information Retrieval. Cambridge University Press.*
3.  **Technical Documentation**:
    *   *Scikit-Learn Documentation*: [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)
    *   *Streamlit API Reference*: [https://docs.streamlit.io/library/api-reference](https://docs.streamlit.io/library/api-reference)
    *   *TMDB API Documentation*: [https://developers.themoviedb.org/3](https://developers.themoviedb.org/3)

---

## 17. Link to Code and Executable

The complete source code, including datasets, python scripts, and documentation, is hosted on GitHub.

*   **GitHub Repository**: [https://github.com/vandana206/Movie_Recommendation-_system](https://github.com/vandana206/Movie_Recommendation-_system)
*   **Clone Command**: `git clone https://github.com/vandana206/Movie_Recommendation-_system.git`
*   **Main Executable File**: `app.py`
