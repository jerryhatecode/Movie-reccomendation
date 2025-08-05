from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import time
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Dummy in-memory movie list per session (no database yet)
user_movie_lists = {}

# TMDB API Key
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY is not set in .env file")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "user" and password == "pass":
            session["username"] = username
            user_movie_lists[username] = user_movie_lists.get(username, [])  # Init list if not present
            return redirect(url_for("welcome"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/welcome")
def welcome():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("welcome.html")

@app.route("/chatbot")
def chatbot():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("chatbot.html")

@app.route('/movielist')
def movie_list():
    if "username" not in session:
        return redirect(url_for("login"))

    genres_to_fetch = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Science Fiction', 'Thriller']

    genre_ids = {
        "action": 28,
        "adventure": 12,
        "animation": 16,
        "comedy": 35,
        "crime": 80,
        "documentary": 99,
        "drama": 18,
        "family": 10751,
        "fantasy": 14,
        "history": 36,
        "horror": 27,
        "music": 10402,
        "mystery": 9648,
        "romance": 10749,
        "sci-fi": 878,
        "science fiction": 878,
        "tv": 10770,
        "thriller": 53,
        "war": 10752,
        "western": 37
    }

    genre_movies = {}

    for genre in genres_to_fetch:
        genre_id = genre_ids.get(genre.lower())
        if genre_id:
            try:
                url = "https://api.themoviedb.org/3/discover/movie"
                params = {
                    "api_key": TMDB_API_KEY,
                    "sort_by": "popularity.desc",
                    "with_genres": genre_id,
                    "language": "en-US"
                }
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                movies = data.get("results", [])[:5]  # Show top 5
                print(f"{genre}: {len(movies)} movies fetched")
                genre_movies[genre] = movies
            except Exception as e:
                print(f"Error fetching {genre}: {e}")
                time.sleep(1)  # pauses the loop for 1 second

                genre_movies[genre] = []
        else:
            genre_movies[genre] = []

    return render_template("list.html", genre_movies=genre_movies)


@app.route('/get-recommendation', methods=['POST'])
def get_recommendation():
    user_message = request.json.get('message', '').lower()

    # Genre detection
    genre_map = {
        "comedy": "35", "funny": "35", "romance": "10749", "action": "28",
        "horror": "27", "drama": "18", "thriller": "53", "sci-fi": "878",
        "science fiction": "878", "animation": "16"
    }
    genre_id = None
    for keyword, g_id in genre_map.items():
        if keyword in user_message:
            genre_id = g_id
            break

    # Keyword detection
    keywords = []
    if "space" in user_message:
        keywords.append("space")
    if "zombie" in user_message:
        keywords.append("zombie")
    if "war" in user_message:
        keywords.append("war")

    # Rating detection
    min_rating = None
    if "above 8" in user_message or "more than 8" in user_message:
        min_rating = 8
    elif "above 7" in user_message:
        min_rating = 7

    # Actor detection (simple example)
    actor_name = None
    if "leonardo dicaprio" in user_message:
        actor_name = "Leonardo DiCaprio"
    elif "emma stone" in user_message:
        actor_name = "Emma Stone"

    # TMDB API setup
    base_url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": 1
    }

    if genre_id:
        params["with_genres"] = genre_id

    if min_rating:
        params["vote_average.gte"] = min_rating

    # Get actor ID if needed
    if actor_name:
        actor_search = requests.get(
            "https://api.themoviedb.org/3/search/person",
            params={"api_key": TMDB_API_KEY, "query": actor_name}
        )
        actor_data = actor_search.json()
        if actor_data.get("results"):
            actor_id = actor_data["results"][0]["id"]
            params["with_cast"] = actor_id

    # Get keyword ID if needed
    if keywords:
        keyword_ids = []
        for kw in keywords:
            kw_search = requests.get(
                "https://api.themoviedb.org/3/search/keyword",
                params={"api_key": TMDB_API_KEY, "query": kw}
            )
            kw_data = kw_search.json()
            if kw_data.get("results"):
                keyword_ids.append(str(kw_data["results"][0]["id"]))
        if keyword_ids:
            params["with_keywords"] = ",".join(keyword_ids)

    # Fetch movies
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            results = response.json().get("results", [])[:3]
            if results:
                movies = [f"{movie['title']} (⭐ {movie['vote_average']})" for movie in results]
                return jsonify({"reply": f"Based on your taste, here are some top picks:\n" + "\n".join(movies)})
            else:
                return jsonify({"reply": "Hmm, I couldn't find any movie matching all that. Try different words?"})
        else:
            return jsonify({"reply": "Oops! TMDB didn’t respond. Try again later."})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Something broke on the backend. Sorry!"}) 
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/profile")
def profile():
    # Example data pulled from session (update keys if different)
    user_data = {
        "username": session.get("username"),
        "email": session.get("email", "user@example.com"),
        "genre": session.get("genre", "Drama"),
        "country": session.get("country", "India"),
        "bio": session.get("bio", "Just a movie lover dreaming big.")
    }
    return render_template("profile.html", user_data=user_data)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":  
    app.run(debug=True)