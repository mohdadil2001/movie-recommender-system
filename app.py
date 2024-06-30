import streamlit as st
import pickle
import pandas as pd
# API = d3938f9c337d78a08228e14abe7353a0
import requests
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=d3938f9c337d78a08228e14abe7353a0&language=en-us'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# Load the movie list and similarity matrix
movies_list = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Extract the movie titles from the DataFrame
movies = movies_list['title'].values
st.title('Movie-Recommender-System')
# Dropdown to select a movie
selected_movie_name = st.selectbox(
    'Select a movie:',
    movies
)

def recommend(movie):
    # Find the index of the selected movie
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    # Get the similarity scores for the selected movie
    distances = similarity[movie_index]
    # Get the indices of the most similar movies
    movies_list_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    # Get the titles of the recommended movies
    recommended_movies = []
    recommended_movies_posters =[]
    for i in movies_list_indices:
        movie_id = movies_list.iloc[i[0]].movie_id
        #fetch poster
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies , recommended_movies_posters

# Button to get recommendations
if st.button('Recommend'):
    name, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])
    with col2:
        st.text(name[1])
        st.image(posters[1])
    with col3:
        st.text(name[2])
        st.image(posters[2])
    with col4:
        st.text(name[3])
        st.image(posters[3])
    with col5:
        st.text(name[4])
        st.image(posters[4])


