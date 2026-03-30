import streamlit as st
from main import recommend, movies

# Page config
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")

# Title
st.title("🎬 Movie Recommendation System")
st.markdown("Get movie recommendations instantly based on your favorite movie!")

# Dropdown instead of text input
selected_movie = st.selectbox(
    "Choose a movie:",
    movies['title'].values
)

# Button
if st.button("Recommend"):
    recommendations = recommend(selected_movie)

    st.subheader(f"Top recommendations for '{selected_movie}':")

    for i, movie in enumerate(recommendations, start=1):
        st.write(f"{i}. {movie}")