import streamlit as st
from main import recommend, movies, get_trending_movies, fetch_movie_full_details

if "selected_movie_details" not in st.session_state:
    st.session_state.selected_movie_details = None
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide"
)

# ---------------- CLEAN WHITE UI ----------------
st.markdown("""
<style>
.stApp {
    background-color: #f8fafc;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: white;
    color: black;
}

/* Buttons */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    font-weight: bold;
}

/* Image styling */
img {
    border-radius: 10px;
}

/* Titles */
h1, h2, h3 {
    color: #111827;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 👨‍💻 Charan Ram Sai")
    st.write("B.Tech CSE (AI & ML) @ SRM KTR")

    st.markdown("""
    <div style="background-color:#f1f5f9;padding:10px;border-radius:10px;">
    AI-powered movie recommendation system using cosine similarity.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("[🔗 GitHub](https://github.com/charankotta32-star)")

# ---------------- HEADER ----------------
st.markdown("<h1>🎬 CineMatch</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:gray;'>Discover movies you'll love — powered by AI</p>", unsafe_allow_html=True)

# ---------------- 🔥 TRENDING ----------------
st.markdown("## 🔥 Trending Now")

trend_names, trend_posters = get_trending_movies()

if trend_names:
    cols = st.columns(5)

    for i in range(len(trend_names)):
        with cols[i]:
            st.image(trend_posters[i], use_container_width=True)
            st.caption(trend_names[i])
else:
    st.warning("⚠️ Unable to load trending movies right now")
# ---------------- SEARCH ----------------
col1, col2 = st.columns([3, 1])

with col1:
    selected_movie = st.selectbox(
        "Search or select a movie:",
        movies['title'].values,
        index=None,
        placeholder="Start typing..."
    )

with col2:
    st.write("")
    st.write("")
    btn = st.button("🎯 Find Matches")

# ---------------- STORE RECOMMENDATION ----------------
if btn and selected_movie:
    result = recommend(selected_movie)

    if result and len(result[0]) > 0:
        st.session_state.recommendations = result
        st.session_state.selected_movie_name = selected_movie
    else:
        st.session_state.recommendations = None


# ---------------- DISPLAY RECOMMENDATION ----------------
if "recommendations" in st.session_state and st.session_state.recommendations:

    names, posters, ratings, years = st.session_state.recommendations
    selected_name = st.session_state.selected_movie_name

    st.markdown(f"## ✨ Because you liked '{selected_name}':")

    cols = st.columns(3)

    for i in range(len(names)):
        with cols[i]:

            # 🖼 Poster
            st.image(posters[i], use_container_width=True)

            # 📌 Title + info
            st.write(f"**{names[i]}**")
            st.caption(f"⭐ {ratings[i]} | 📅 {years[i]}")

            # 🔥 Button (WORKING)
            if st.button(f"View Details - {names[i]}", key=f"btn_{names[i]}"):
                data = fetch_movie_full_details(names[i])

                if data:
                    st.session_state.selected_movie_details = data
                else:
                    st.warning("⚠️ Failed to fetch movie details")

# ---------------- DETAILS ----------------
if st.session_state.selected_movie_details:

    movie = st.session_state.selected_movie_details

    if movie:
        st.markdown("---")
        st.markdown(f"## 🎬 {movie['title']} ({movie['year']})")
        st.write(f"⭐ Rating: {movie['rating']}")
        st.write(movie['overview'])

        if movie["trailer"]:
            st.video(movie["trailer"])
    else:
        st.warning("⚠️ Movie details not found")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<center style='color:gray;'>Built with ❤️ using Python & Streamlit | 2026</center>",
    unsafe_allow_html=True
)
