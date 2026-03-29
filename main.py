import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import streamlit as st

# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():
    url_movies = "https://drive.google.com/uc?id=1Scd4KMJqpYO6UynA2ax99ow9YtsnX8MM"
    url_credits = "https://drive.google.com/uc?id=1eQO0d3K3B7t9Ptjj0gG2myX01WD0BwFc"

    movies = pd.read_csv(url_movies)
    credits = pd.read_csv(url_credits)

    return movies, credits
movies, credits = load_data()
# ---------------- MERGE & SELECT ----------------

movies = movies.merge(credits, on='title')
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.dropna(inplace=True)

# ---------------- HELPER FUNCTIONS ----------------

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

# ---------------- DATA PROCESSING ----------------

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

# ---------------- STEMMING ----------------

ps = PorterStemmer()

def stem(text):
    return " ".join([ps.stem(word) for word in text.split()])

movies['tags'] = movies['tags'].apply(stem)

# ---------------- VECTORIZE ----------------

@st.cache_data
def create_similarity(data):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(data['tags']).toarray()
    similarity = cosine_similarity(vectors)
    return similarity

similarity = create_similarity(movies)

# ---------------- RECOMMEND FUNCTION ----------------

def recommend(movie):
    movie = movie.title()

    if movie not in movies['title'].values:
        return ["Movie not found ❌"]

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),
                         reverse=True,
                         key=lambda x: x[1])[1:10]

    recommendations = []
    seen = set()

    for i in movies_list:
        title = movies.iloc[i[0]].title
        if title not in seen:
            recommendations.append(title)
            seen.add(title)

    return recommendations