import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=ec4a6c1a67bfc4b7b62d847cf453d006"
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        poster_path = data.get('poster_path')  # Use get to avoid KeyError
        if poster_path:
            full_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return full_url
        else:
            return "https://via.placeholder.com/500"  # Return a placeholder image if no poster is found
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500"  # Return a placeholder image in case of error

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommendation System")

selectvalue = st.selectbox("Select movie from the below dropdown menu", movies_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_movie_poster = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommend_movie_poster.append(fetch_poster(movie_id))
        recommend_movie.append(movies.iloc[i[0]].title)
    return recommend_movie, recommend_movie_poster

if st.button("Show recommended movies"):
    movie_title, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_title[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_title[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_title[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_title[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_title[4])
        st.image(movie_poster[4])
