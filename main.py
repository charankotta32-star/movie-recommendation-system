import pandas as pd
import ast
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import streamlit as st
import nltk

nltk.download('punkt')
API_KEY = "16519757e8bfd9b60561ad9b7dca4dc2"
# ================== LOAD DATA ==================

@st.cache_data
def load_data():
    url_movies = "https://drive.google.com/uc?id=1Scd4KMJqpYO6UynA2ax99ow9YtsnX8MM"
    url_credits = "https://drive.google.com/uc?id=1eQO0d3K3B7t9Ptjj0gG2myX01WD0BwFc"

    movies = pd.read_csv(url_movies)
    credits = pd.read_csv(url_credits)

    return movies, credits


movies, credits = load_data()

# ================== MERGE ==================

movies = movies.merge(credits, on='title')
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.dropna(inplace=True)

# ================== HELPERS ==================

def convert(text):
    return [i['name'] for i in ast.literal_eval(text)]

def convert_cast(text):
    return [i['name'] for i in ast.literal_eval(text)[:3]]

def fetch_director(text):
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            return [i['name']]
    return []

def remove_space(lst):
    return [i.replace(" ", "") for i in lst]

# ================== PROCESS ==================

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_cast)
movies['crew'] = movies['crew'].apply(fetch_director)

movies['genres'] = movies['genres'].apply(remove_space)
movies['keywords'] = movies['keywords'].apply(remove_space)
movies['cast'] = movies['cast'].apply(remove_space)
movies['crew'] = movies['crew'].apply(remove_space)

movies['overview'] = movies['overview'].apply(lambda x: x.split())

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))

# ================== STEMMING ==================

ps = PorterStemmer()

def stem(text):
    return " ".join([ps.stem(word) for word in text.split()])

movies['tags'] = movies['tags'].apply(stem)

# ================== VECTORIZE ==================

@st.cache_data
def create_similarity(data):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(data['tags']).toarray()
    similarity = cosine_similarity(vectors)
    return similarity

similarity = create_similarity(movies)

# ================== 🎬 POSTER FETCH ==================

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        poster_path = data.get("poster_path")
        rating = data.get("vote_average", "N/A")
        release_date = data.get("release_date", "")

        year = release_date[:4] if release_date else "N/A"

        poster = (
            f"https://image.tmdb.org/t/p/w500{poster_path}"
            if poster_path
            else "https://via.placeholder.com/300x450?text=No+Image"
        )

        return poster, rating, year

    except Exception:
        return "https://via.placeholder.com/300x450?text=Error", "N/A", "N/A"

# ================== 🎯 RECOMMEND ==================

def recommend(movie):
    movie = movie.lower()

    # Flexible match
    matches = movies[movies['title'].str.lower().str.contains(movie)]

    if matches.empty:
        return [], []

    movie_index = matches.index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:10]   # take more, filter later

    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []
    recommended_years = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title

        poster, rating, year = fetch_movie_details(movie_id)

        if "placeholder" in poster:
            continue

        recommended_movies.append(title)
        recommended_posters.append(poster)
        recommended_ratings.append(rating)
        recommended_years.append(year)

        if len(recommended_movies) == 3:
            break

    return recommended_movies, recommended_posters, recommended_ratings, recommended_years

@st.cache_data(ttl=3600)
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        trending_names = []
        trending_posters = []

        for movie in data.get("results", [])[:5]:
            title = movie.get("title")
            poster_path = movie.get("poster_path")

            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                trending_names.append(title)
                trending_posters.append(poster_url)

        return trending_names, trending_posters

    except Exception:
        return [], []

def fetch_movie_full_details(movie_name):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"

    try:
        data = requests.get(search_url).json()

        results = data.get("results")
        if not results:
            return None

        movie = results[0]
        movie_id = movie.get("id")

        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        videos_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"

        details = requests.get(details_url).json()
        videos = requests.get(videos_url).json()

        trailer_key = None
        for v in videos.get("results", []):
            if v.get("type") == "Trailer" and v.get("site") == "YouTube":
                trailer_key = v.get("key")
                break

        return {
            "title": details.get("title"),
            "overview": details.get("overview"),
            "rating": details.get("vote_average"),
            "year": details.get("release_date", "")[:4],
            "trailer": f"https://www.youtube.com/watch?v={trailer_key}" if trailer_key else None
        }

    except Exception as e:
        print("ERROR:", e)
        return None
