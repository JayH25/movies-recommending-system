import pickle
import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="CineMatch - Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #f1f8ff, #e3f2fd);
    }

    .movie-title {
        font-weight: 600;
        color: #4a148c;
        margin-top: 0.5rem;
        text-align: center;
        font-size: 0.9rem;
        line-height: 1.2;
        height: 2.4rem; /* Force enough height for 2 lines */
        overflow: hidden;
    }

    .stSelectbox > div > div {
        color: black !important;
    }

    .stSelectbox label {
        font-weight: 600;
        color: #2c3e50 !important;
    }

    h1 {
        color: #2c3e50;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    footer, header, #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# Function to fetch poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url, timeout=10).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w300/" + poster_path  # smaller size for better layout
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    except:
        return "https://via.placeholder.com/300x450?text=No+Image"

# Recommend function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:11]:  # 10 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Header
st.markdown("<h1>🎬 CineMatch</h1>", unsafe_allow_html=True)
st.write("#### Discover your next favorite movie")

# Select box
movie_list = movies['title'].values
selected_movie = st.selectbox("🎞️ Type or select a movie", movie_list)

# Show recommendations
if st.button('✨ Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display in two rows of 5
    for row in range(2):  # 2 rows
        cols = st.columns(5)
        for i in range(5):
            idx = row * 5 + i
            if idx < len(recommended_movie_names):
                with cols[i]:
                    st.image(recommended_movie_posters[idx], use_container_width=True)

                    st.markdown(f'<p style="color:#fffff; font-weight:600; text-align:center;">{recommended_movie_names[idx]}</p>', unsafe_allow_html=True)


# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #fffff; font-size: 0.9rem;">Made with ❤️ using Streamlit & TMDB API</p>',
    unsafe_allow_html=True
)
