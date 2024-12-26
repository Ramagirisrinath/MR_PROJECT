# Import necessary libraries
import streamlit as st
import pickle
import requests

# Function to fetch the movie poster using TMDB API
def fetch_poster(movie_id):
    try:
        # API URL to fetch movie details
        url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
        response = requests.get(url)  # Send a GET request to the API
        if response.status_code == 200:  # Check if the response is successful
            data = response.json()  # Parse JSON response
            poster_path = data.get('poster_path')  # Extract poster path
            if poster_path:  # If a poster path exists
                full_path = "https://image.tmdb.org/t/p/w500/" + poster_path  # Construct full URL for the poster
                return full_path
            else:
                return None  # No poster path found
        else:
            return None  # API response unsuccessful
    except Exception as e:
        print("Error fetching poster:", e)  # Print error if the request fails
        return None

# Function to recommend movies based on the selected movie
def recommend(movie):
    try:
        # Find the index of the selected movie in the dataset
        index = movies[movies['title'] == movie].index[0]
        
        # Calculate similarity scores for the selected movie
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
        
        # Lists to store recommended movie titles and posters
        recommend_movie = []
        recommend_poster = []
        
        # Fetch the top 5 similar movies
        for i in distance[1:6]:
            movies_id = movies.iloc[i[0]].id  # Get movie ID
            recommend_movie.append(movies.iloc[i[0]].title)  # Append movie title
            
            # Fetch poster for the recommended movie
            poster = fetch_poster(movies_id)
            if poster:
                recommend_poster.append(poster)  # Append poster URL
            else:
                recommend_poster.append("Poster not available")  # Handle missing posters
        return recommend_movie, recommend_poster
    except IndexError:
        print("Movie not found in dataset")  # Handle case where movie is not in the dataset
        return [], []  # Return empty lists if recommendation fails

# Load pre-saved movie data and similarity matrix
movies = pickle.load(open("movies_list", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_lists = movies['title'].values  # Extract movie titles

# Streamlit application header
st.header("Movie Recommender System")

# Import Streamlit's custom component functionality
import streamlit.components.v1 as components

# Declare a custom component for an image carousel
imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

# Pre-fetch example movie posters for the carousel
imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
]

# Display the image carousel
imageCarouselComponent(imageUrls=imageUrls, height=200)

# Dropdown to select a movie from the list
selectvalue = st.selectbox("Select movie from dropdown", movies_lists)

# Button to trigger movie recommendations
if st.button("Show Recommend"):
    # Get recommendations for the selected movie
    movie_name, movie_poster = recommend(selectvalue)
    
    # Create 5 columns to display recommended movies and posters
    col1, col2, col3, col4, col5 = st.columns(5)
    for i in range(5):
        with globals()[f"col{i+1}"]:  # Dynamically access column by name
            if i < len(movie_name):  # Ensure index is within bounds
                st.text(movie_name[i])  # Display movie title
                if movie_poster[i] != "Poster not available":
                    st.image(movie_poster[i])  # Display poster image
                else:
                    st.write(movie_poster[i])  # Display fallback text for missing posters
