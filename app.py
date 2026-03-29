import streamlit as st
from main import recommend

st.set_page_config(page_title="Movie Recommender", page_icon="🎬")

st.title("🎬 Movie Recommendation System")
st.write("Get movie recommendations based on similarity 🎯")

movie_name = st.text_input("Enter a movie name:")

if st.button("Recommend"):
    if movie_name:
        results = recommend(movie_name)

        st.subheader("🎥 Recommendations:")

        for movie in results:
            st.write(f"👉 {movie}")
    else:
        st.warning("Please enter a movie name.")