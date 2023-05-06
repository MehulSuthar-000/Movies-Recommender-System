import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=1d87866cb4ffcf4d0829921cd12cac9f&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']

def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)) , reverse=True , key=lambda x:x[1])[1:6]
    
    recommended = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetching poster from API
        recommended.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended,recommended_movies_poster
    


similarity = pickle.load(open('movies_similarity.pkl' , 'rb'))
movies = pickle.load(open("movies.pkl" , 'rb'))
movies = pd.DataFrame(movies)
movies_title = movies['title'].values
st.title("Movie-Recommender-System")

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    (movies_title))

if st.button('Recommend Movies'):
    recommendations,poster = recommend(selected_movie_name)
    col1, col2, col3 ,col4 , col5 = st.columns(5)

    with col1:
       st.text(recommendations[0])
       st.image(poster[0])
    with col2:
       st.text(recommendations[1])
       st.image(poster[1])
    with col3:
       st.text(recommendations[2])
       st.image(poster[2])
    with col4:
       st.text(recommendations[3])
       st.image(poster[3])
    with col5:
       st.text(recommendations[4])
       st.image(poster[4])

