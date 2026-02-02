import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Ensure NLTK data is downloaded
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt') # Just in case

# Load credits data globally
credits_df = None

def load_credits_data(filepath="tmdb_5000_credits.csv"):
    """Load the credits CSV with actor/actress information."""
    global credits_df
    try:
        credits_df = pd.read_csv(filepath)
    except:
        credits_df = None

def get_cast_from_credits(movie_id):
    """Get cast information from credits data."""
    if credits_df is None:
        return ""
    try:
        cast_row = credits_df[credits_df['movie_id'] == movie_id]
        if not cast_row.empty:
            cast_str = cast_row['cast'].iloc[0]
            cast_list = json.loads(cast_str)
            # Get top 2 actors
            actors = [actor['name'] for actor in cast_list[:2]]
            return ", ".join(actors)
    except:
        pass
    return ""

def load_data(filepath="tmdb_5000_movies.csv"):
    """Loads the dataset and handles missing values."""
    df = pd.read_csv(filepath)
    # Fill NaN values with empty strings for text columns
    df['overview'] = df['overview'].fillna('')
    df['genres'] = df['genres'].fillna('[]')
    df['keywords'] = df['keywords'].fillna('[]')
    return df

def parse_json_column(json_str):
    """Extracts names from JSON-like columns (genres, keywords)."""
    try:
        data = json.loads(json_str)
        return " ".join([item['name'] for item in data])
    except:
        return ""

def clean_text(text):
    """Applies NLP techniques: Lowercasing, Stop-words removal, Lemmatization."""
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    # Lowercase
    text = text.lower()
    
    # Tokenize (simple split here is often enough for this use case, or use word_tokenize)
    words = text.split()
    
    # Remove stopwords and lemmatize
    cleaned_words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    
    return " ".join(cleaned_words)

def prepare_data(df):
    """Combines features and cleans text."""
    # Extract text from JSON columns
    df['genre_names'] = df['genres'].apply(parse_json_column)
    df['keyword_names'] = df['keywords'].apply(parse_json_column)
    
    # Combine features
    df['combined_features'] = df['genre_names'] + " " + df['keyword_names'] + " " + df['overview']
    
    # Clean text
    df['cleaned_text'] = df['combined_features'].apply(clean_text)
    
    return df

def build_similarity_matrix(df):
    """Vectorizes text and calculates cosine similarity."""
    tfidf = TfidfVectorizer(max_features=5000) # Limit features for performance
    tfidf_matrix = tfidf.fit_transform(df['cleaned_text'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

def get_recommendations(title, df, cosine_sim):
    """Returns top 10 recommended movies based on similarity."""
    try:
        # Get index of the movie
        idx = df[df['title'].str.lower() == title.lower()].index[0]
        
        # Get similarity scores
        sim_scores = list(enumerate(cosine_sim[idx]))
        
        # Sort by score
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top 30 (to allow filtering later)
        sim_scores = sim_scores[1:31]
        
        # Get movie indices
        movie_indices = [i[0] for i in sim_scores]
        
        # Return rich data
        results = []
        for i, score in zip(movie_indices, [s[1] for s in sim_scores]):
            movie_id = df['id'].iloc[i]
            cast_info = get_cast_from_credits(movie_id)
            results.append({
                'title': df['title'].iloc[i],
                'overview': df['overview'].iloc[i],
                'release_date': df['release_date'].iloc[i],
                'vote_average': df['vote_average'].iloc[i],
                'genres': df['genres'].iloc[i],
                'similarity': score,
                'id': movie_id,
                'cast': cast_info  # Add cast information
            })
        return results
    except IndexError:
        return []
