import requests
import streamlit as st
import pickle

st.set_page_config(
    page_title="MovieLens AI",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
            
.block-container {
    padding-top: 0rem;
}
            
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main background */
.stApp {
    background-color: #0E1117;
    color: white;
}

/* Dropdown */
div[data-baseweb="select"] > div {
    background-color: #262730;
    color: white;
}

/* Buttons */
.stButton > button {
    background-color: #FF4B4B;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.5rem 1rem;
}

.stButton > button:hover {
    background-color: #E63946;
}

/* Center movie titles */
.movie-title {
    text-align: center;
    font-weight: bold;
    color: white;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <h1 style='text-align:center;
               font-size:3rem;
               font-weight:700;'>
        🎬 MovieLens AI
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center;
              color:#B0B0B0;
              font-size:1.1rem;'>
        Discover movies you'll love with AI-powered content-based recommendations.
    </p>
    """,
    unsafe_allow_html=True
)


movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4e4c25c091028ac4469258dbdc7560eb"

    data = requests.get(url)

    data = data.json()

    poster_path = data.get('poster_path')
    rating = data.get('vote_average')
    overview = data.get('overview')

    if poster_path:

        poster_url = (
           "https://image.tmdb.org/t/p/w500/"
            + poster_path
        )
        return poster_url, rating, overview

    return None, None, None

from difflib import get_close_matches

def recommend(movie):

    movie_titles = movies['title'].tolist()

    # Exact match check
    movie_data = movies[
        movies['title'].str.lower() == movie.lower()
    ]

    if movie_data.empty:

        matches = get_close_matches(
            movie,
            movie_titles,
            n=5,
            cutoff=0.6
        )

        print(f"'{movie}' not found in dataset.")

        if matches:
            print("\nDid you mean:")
            for m in matches:
                print(m)

        return

    movie_index = movie_data.index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []
    recommended_overviews = []

    for index, score in movies_list:

        movie_id = movies.iloc[index].movie_id

        recommended_movies.append(
           movies.iloc[index].title
        )

        poster, rating, overview = fetch_poster(movie_id)

        recommended_posters.append(poster)
        recommended_ratings.append(rating)
        recommended_overviews.append(overview)
        

    return(
           recommended_movies,
           recommended_posters,
           recommended_ratings,
           recommended_overviews
        )

 
movie_list = movies['title'].values

st.markdown(
    "<h4 style='color:white;'>Choose a Movie 🎥</h4>",
    unsafe_allow_html=True
)

selected_movie = st.selectbox(
    "",
    movie_list
)

if st.button("🎬 Recommend Movies"):

    with st.spinner("Finding similar movies... 🍿"):

        names, posters, ratings, overviews = recommend(selected_movie)

    st.subheader(f"Movies Similar to {selected_movie}")

    col1, col2, col3, col4, col5 = st.columns(5)

    cols = [col1, col2, col3, col4, col5]

    for i in range(len(names)):

        with cols[i]:
            
            st.image(posters[i], use_container_width=True)

            st.markdown(
                f"<div style='text-align:center'><b>{names[i]}</b></div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='text-align:center;font-size:18px;'>⭐ {ratings[i]:.1f}</div>",
                unsafe_allow_html=True
            )
            overview_text = (
                overviews[i][:100] + "..."
                if overviews[i]
                else "No description available."
            )
            st.caption(overview_text)

