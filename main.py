import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer

# ---------------- LOAD DATA ----------------
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

movies = movies.merge(credits, on='title')

movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.dropna(inplace=True)

# ---------------- HELPER FUNCTIONS ----------------

def convert(text):
    return [i['name'] for i in ast.literal_eval(text)]

def convert_cast(text):
    L = []
    for i, item in enumerate(ast.literal_eval(text)):
        if i < 3:
            L.append(item['name'])
        else:
            break
    return L

def fetch_director(text):
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            return [i['name']]
    return []

def remove_space(L):
    return [i.replace(" ", "") for i in L]

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

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# ---------------- SIMILARITY ----------------

similarity = cosine_similarity(vectors)

# ---------------- RECOMMEND FUNCTION ----------------

def recommend(movie):
    movie = movie.title()

    if movie not in movies['title'].values:
        return ["Movie not found ❌"]

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]

    seen = set()
    recommendations = []

    for i in movies_list:
        name = movies.iloc[i[0]].title
        if name not in seen:
            recommendations.append(name)
            seen.add(name)

    return recommendations