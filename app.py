import streamlit as st
import pickle

st.title("🎬 Movie Recommender System")
# st.markdown("""
# <style>
# div[data-baseweb="select"] {
#     cursor: pointer;
# }
# </style>
# """, unsafe_allow_html=True)

movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

new_df = movies

from difflib import get_close_matches

def recommend(movie):

    movie_titles = new_df['title'].tolist()

    # Exact match check
    movie_data = new_df[
        new_df['title'].str.lower() == movie.lower()
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

    for i in movies_list:
        recommended_movies.append(
           new_df.iloc[i[0]].title
        )

    return recommended_movies

 
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Choose a movie",
    movie_list
)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)

    for movie in recommendations:
        st.write(movie)


