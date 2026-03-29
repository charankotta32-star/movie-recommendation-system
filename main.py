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
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

def convert_cast(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L

def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

def remove_space(L):
    return [i.replace(" ", "") for i in L]

# ---------------- DATA PROCESSING ----------------

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_cast)
movies['crew'] = movies['crew'].apply(fetch_director)

# remove spaces
movies['genres'] = movies['genres'].apply(remove_space)
movies['keywords'] = movies['keywords'].apply(remove_space)
movies['cast'] = movies['cast'].apply(remove_space)
movies['crew'] = movies['crew'].apply(remove_space)

# split overview
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# combine all features
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# convert list to string
movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))

# ---------------- STEMMING ----------------

ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

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
        print("Movie not found ❌")
        return

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]

    seen = set()
    print(f"\n🎬 Recommendations for '{movie}':\n")

    for i in movies_list:
        name = movies.iloc[i[0]].title
        if name not in seen:
            print(name)
            seen.add(name)

# ---------------- TEST ----------------

recommend("Avatar")
recommend("Batman Begins")
recommend("Titanic")