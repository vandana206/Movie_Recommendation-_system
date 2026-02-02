import streamlit as st
import recommender
import pandas as pd
import json
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Initialize session state for poster cache
if 'poster_cache' not in st.session_state:
    st.session_state.poster_cache = {}

if 'cast_cache' not in st.session_state:
    st.session_state.cast_cache = {}

if 'tmdb_api_key' not in st.session_state:
    st.session_state.tmdb_api_key = "8265bd1679663a7ea12ac168da84d2e8"

def get_gradient_colors(title):
    """Generates muted/darker gradient colors for movie posters"""
    gradients = [
        # Dark Reds
        ('linear-gradient(135deg, #8b0000 0%, #b22222 100%)', '#8b0000'),
        ('linear-gradient(135deg, #6b0000 0%, #8b3a3a 100%)', '#6b0000'),
        # Dark Blues
        ('linear-gradient(135deg, #000080 0%, #1e3a8a 100%)', '#000080'),
        ('linear-gradient(135deg, #1a3a4a 0%, #2c5aa0 100%)', '#1a3a4a'),
        # Dark Greens
        ('linear-gradient(135deg, #004d00 0%, #1b5e20 100%)', '#004d00'),
        ('linear-gradient(135deg, #1a4d2e 0%, #2d6a4f 100%)', '#1a4d2e'),
        # Dark Purples
        ('linear-gradient(135deg, #2d0a4e 0%, #44337a 100%)', '#2d0a4e'),
        ('linear-gradient(135deg, #3d0066 0%, #5d3a8c 100%)', '#3d0066'),
        # Dark Oranges
        ('linear-gradient(135deg, #8b4513 0%, #a0522d 100%)', '#8b4513'),
        ('linear-gradient(135deg, #663300 0%, #8b4500 100%)', '#663300'),
    ]
    idx = hash(title) % len(gradients)
    return gradients[idx]

# Function to fetch cast information
def get_cast_info(movie_id):
    """Fetch cast information from TMDB API with fallback"""
    # Check cache first
    if movie_id in st.session_state.cast_cache:
        return st.session_state.cast_cache[movie_id]
    
    try:
        api_key = st.session_state.get('tmdb_api_key', "8265bd1679663a7ea12ac168da84d2e8")
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
        
        session = requests.Session()
        retry = Retry(connect=2, backoff_factor=0.3)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        response = session.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            cast = data.get('cast', [])
            # Get top 3 actors
            top_actors = [actor['name'] for actor in cast[:3]]
            cast_text = ", ".join(top_actors)
            st.session_state.cast_cache[movie_id] = cast_text
            return cast_text
    except Exception as e:
        pass
    
    st.session_state.cast_cache[movie_id] = "Cast info unavailable"
    return "Cast info unavailable"



# Page Config
st.set_page_config(
    page_title="Cinematch AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to fetch poster URL
def get_poster_url(movie_id):
    """Fetch poster URL from TMDB API"""
    # Check cache first
    if movie_id in st.session_state.poster_cache:
        return st.session_state.poster_cache[movie_id]
    
    try:
        api_key = st.session_state.get('tmdb_api_key', "8265bd1679663a7ea12ac168da84d2e8")
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        
        # Add retry logic
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        response = session.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                st.session_state.poster_cache[movie_id] = poster_url
                return poster_url
    except Exception as e:
        pass
    
    # Return None if poster not found
    st.session_state.poster_cache[movie_id] = None
    return None

# --- Custom CSS for Premium Design & fixes ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
    }

    /* FIX: Selectbox Visibility */
    div[data-baseweb="select"] > div {
        background-color: #21262d !important;
        border-color: #30363d !important;
        color: white !important;
    }
    div[data-baseweb="select"] span {
        color: white !important;
    }
    ul[data-testid="stSelectboxVirtualDropdown"] li {
        background-color: #21262d !important;
        color: white !important;
    }

    /* FIX: Sidebar Text Visibility (Radio Buttons, Labels) */
    .stRadio label, .stSelectbox label {
        color: #ffffff !important;
        font-size: 1rem;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #e6edf3 !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #b81d24, #8a151b);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 4px;
        font-weight: bold;
        transition: all 0.2s ease-in-out;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(184, 29, 36, 0.4);
    }

    /* Metric/Badge Styling */
    .badge {
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 8px;
        color: white;
    }
    .badge-rating { background-color: #1f6feb; }
    .badge-date { background-color: #238636; }
    .badge-similarity { background-color: #6e40c9; }

    /* Movie Card */
    .movie-card {
        background-color: #21262d;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 0;
        margin-bottom: 20px;
        overflow: hidden;
        transition: transform 0.3s ease, border-color 0.3s ease;
        display: flex;
        height: 280px;
        flex-direction: row;
        height: 220px;
    }
    .movie-card:hover {
        transform: translateY(-4px);
        border-color: #8b949e;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }
    
    /* Poster Placeholder */
    .poster-placeholder {
        width: 200px;
        min-width: 200px;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        font-weight: bold;
        color: rgba(255,255,255,0.4);
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        border-radius: 8px 0 0 8px;
    }
    
    .poster-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 8px 0 0 8px;
    }

    /* Card Content */
    .card-content {
        padding: 20px;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }
    .card-title {
        font-size: 1.4rem;
        color: #ffffff;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .card-meta {
        margin-bottom: 12px;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    .card-desc {
        font-size: 0.9rem;
        color: #8b949e;
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    /* Grid Layout Styles */
    .grid-movie-card {
        background-color: #21262d;
        border: 1px solid #30363d;
        border-radius: 8px;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
    }
    
    .grid-movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 24px rgba(0,0,0,0.6);
        border-color: #8b949e;
    }
    
    .grid-card-header {
        padding: 10px 12px;
        background-color: #161b22;
        border-bottom: 1px solid #30363d;
    }
    
    .grid-poster-container {
        width: 100%;
        height: 280px;
        overflow: hidden;
        background-color: #161b22;
    }
    
    .grid-poster-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }
    
    .grid-card-title {
        font-size: 0.95rem;
        color: #ffffff;
        font-weight: 600;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        line-height: 1.3;
    }
    
    .grid-card-footer {
        padding: 10px 12px;
        background-color: #161b22;
        border-top: 1px solid #30363d;
    }
    
    .grid-card-cast {
        font-size: 0.8rem;
        color: #60a5fa;
        margin-bottom: 6px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
        line-height: 1.2;
        font-weight: 500;
    }
    
    .grid-card-rating {
        font-size: 0.9rem;
        color: #fbbf24;
        margin-bottom: 6px;
        font-weight: 600;
    }
    
    .grid-card-match {
        font-size: 0.9rem;
        color: #a78bfa;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Data Loading
@st.cache_data
def get_data_and_sim():
    # Load credits data first
    recommender.load_credits_data()
    
    df = recommender.load_data()
    df = recommender.prepare_data(df)
    sim = recommender.build_similarity_matrix(df)
    # Parse genres for filtering
    df['parsed_genres'] = df['genres'].apply(lambda x: [g['name'] for g in json.loads(x)] if isinstance(x, str) else [])
    # Get unique genres list
    all_genres = set()
    for genres in df['parsed_genres']:
        all_genres.update(genres)
    return df, sim, sorted(list(all_genres))

    # --- Main Layout ---

st.markdown("""
    <div style='text-align: center; padding: 20px 0 40px 0;'>
        <h1 style='font-size: 3rem; margin-bottom: 10px;'>🎬 Cinematch AI</h1>
        <p style='font-size: 1.2rem; color: #8b949e;'>Discover your next favorite film</p>
    </div>
""", unsafe_allow_html=True)

try:
    with st.spinner('Loading database...'):
        df, cosine_sim, all_genres = get_data_and_sim()

    # --- Sidebar ---
    with st.sidebar:
        st.header("Search")
        
        # 1. Movie Selection
        movie_list = sorted(df['title'].values)
        selected_movie = st.selectbox(
            "Select a Reference Movie:",
            movie_list,
            index=movie_list.index("Avatar") if "Avatar" in movie_list else 0
        )

        # Advanced Settings (Hidden by default to avoid confusion)
        with st.expander("⚙️ Advanced Settings"):
            user_api_key = st.text_input("Custom TMDB API Key", type="password", help="Optional: Use your own key if the default one hits limits.")
            
            # Use user key if provided, otherwise default
            if user_api_key:
                st.session_state.tmdb_api_key = user_api_key
            else:
                st.session_state.tmdb_api_key = "8265bd1679663a7ea12ac168da84d2e8"  # Working Default Key
        
        st.markdown("---")
        st.header("Filters")
        
        # 2. Genre Filter
        selected_genre = st.selectbox(
            "Filter by Genre:",
            ["All Genres"] + all_genres
        )
        
        # 3. Sort Order
        sort_option = st.radio(
            "Sort Results By:",
            ("Match Confidence", "High Rating", "Newest Release")
        )
        
        st.markdown("---")
        find_btn = st.button('🔍 Find Similar Movies')

    # --- Logic ---
    if find_btn:
        st.subheader(f"Movies similar to: {selected_movie}")
        
        # Get raw recommendations (top 30)
        raw_recs = recommender.get_recommendations(selected_movie, df, cosine_sim)
        
        if raw_recs:
            filtered_recs = []
            
            # Application of Filters
            for movie in raw_recs:
                # Genre Filter
                movie_genres = [g['name'] for g in json.loads(movie['genres'])] if isinstance(movie['genres'], str) else []
                if selected_genre != "All Genres" and selected_genre not in movie_genres:
                    continue
                filtered_recs.append(movie)
            
            # Application of Sorting
            if sort_option == "High Rating":
                filtered_recs.sort(key=lambda x: x['vote_average'], reverse=True)
            elif sort_option == "Newest Release":
                # Handle NaNs or bad dates loosely
                filtered_recs.sort(key=lambda x: str(x['release_date']), reverse=True)
            else: # Match Confidence (already sorted by default from recommender, but good to ensure)
                filtered_recs.sort(key=lambda x: x['similarity'], reverse=True)
            
            # Limit to top 10 after filtering
            final_recs = filtered_recs[:10]
            
            if final_recs:
                # Create grid layout
                cols = st.columns(5)
                for idx, movie in enumerate(final_recs):
                    with cols[idx % 5]:
                        bg_gradient, accent_color = get_gradient_colors(movie['title'])
                        initials = "".join([x[0] for x in movie['title'].split()[:2]]).upper()
                        
                        # Fetch poster URL
                        poster_url = get_poster_url(movie['id'])
                        
                        # Fetch Cast Info (Live)
                        cast_names = get_cast_info(movie['id'])

                        # Create poster HTML
                        if poster_url:
                            poster_html = f'<img src="{poster_url}" class="grid-poster-img" alt="{movie["title"]}">'
                        else:
                            poster_html = f'<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 280px; background: {bg_gradient}; font-size: 3.5rem; font-weight: bold; border-radius: 8px; color: rgba(255,255,255,0.95); text-shadow: 0 2px 8px rgba(0,0,0,0.5);">{initials}</div>'
                        
                        st.markdown(f"""
                        <div class="grid-movie-card">
                            <div class="grid-card-header">
                                <div class="grid-card-title">{movie['title']}</div>
                            </div>
                            <div class="grid-poster-container">
                                {poster_html}
                            </div>
                            <div class="grid-card-footer">
                                <div class="grid-card-cast" title="{cast_names}">Cast: {cast_names}</div>
                                <div class="grid-card-rating">★ {movie['vote_average']}</div>
                                <div class="grid-card-match">{(movie['similarity']*100):.1f}% Match</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning(f"No movies found matching genre '{selected_genre}' similar to '{selected_movie}'.")
        else:
            st.error("Could not find recommendations.")
            
    else:
        # Initial State - Fixed visibility and message
        st.markdown("""
        <div style='background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; text-align: center; color: #8b949e;'>
            <h3 style='color: #e6edf3 !important;'>Welcome to Cinematch AI</h3>
            <p> Select a movie from the sidebar and click <strong>Find Similar Movies</strong> to start!</p>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"An error occurred: {e}")
