# Movie Recommendation Web App

This is a personal movie recommendation web app built using Flask. It allows users to get movie suggestions based on genres, save them to a watchlist, and explore additional features through a chatbot. The interface is simple, with an elegant homepage and a dark-themed chatbot.

## Features

- User signup and login system
- Genre-based movie recommendations using TMDB API
- Movie chatbot with free-text input
- Add, view, and delete movies from the watchlist
- About page with personal vision
- Profile page showing user details
- Stylish UI with custom CSS and animations

## How to Run the Project

1. **Clone the Repository**
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name


2. **Create and Activate Virtual Environment (optional)**
python -m venv venv
venv\Scripts\activate (Windows)
source venv/bin/activate (Linux/Mac)

markdown
Copy
Edit

3. **Install Required Packages**
pip install -r requirements.txt

markdown
Copy
Edit

4. **Add your TMDB API key**
- Create a `.env` file in the root directory
- Add the line:
  ```
  TMDB_API_KEY=your_api_key_here
  ```

5. **Run the Flask App**
python app.py


6. **Open in browser**
- Visit `http://localhost:5000` in your browser

 **How to Get TMDB API Key (v3 and v4)**
Step 1: Create a TMDB Account
Go to https://www.themoviedb.org/

Click on "Login" (top right) and Sign Up if you don’t have an account.

Step 2: Apply for an API Key
After logging in, go to: https://www.themoviedb.org/settings/api

Click "Create" or "Request an API Key"

Choose Developer option when asked about your purpose.

Fill out the basic details (name, purpose, app name, etc.)

Step 3: Get the API Key
After approval, you will receive:

API Key v3 (key format: xxxxxxxxxxxxxxxxxxxxxx) — this is used in most cases

API Key v4 (Bearer Token format: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...) — used with authorization headers


## Project Structure

movie-recommendation-app/
│
├── static/
│ ├── css/
│ │ ├── home.css
│ │ ├── about.css
│ │ ├── profile.css
│ │ └── login.css
│ │ ├── chatbot.css
│ │ ├── movielist.css
│ ├── js/
│ │ ├── home.js
│ │ ├── about.js
│ │ ├── profile.js
│ │ └── login.js
│ │ ├── chatbot.js
│ │ ├── movielist.js
│
├── templates/
│ ├── home.html
│ ├── about.html
│ ├── profile.html
│ ├── login.html
│ └── welcome.html
│ └──chatbot.html
│ └── movielist.html
│
├── app.py
├── .env
├── requirements.txt
└── README.md


## Notes

- Do not share your `.env` file publicly if it contains sensitive API keys.
- The project is meant for personal and educational use.
- This project uses the **TMDB API v3** token for fetching movies.
- If you want to use **v4**, make sure to generate a Bearer Token (read-only) from your TMDB account and update the headers accordingly in the code.
- TMDB has **API rate limits**, so sometimes movie data may not load due to connection errors or hitting the request limit.
- For better error handling, you can add try-catch blocks or display custom fallback messages.


## License

This project is open source. You can modify or distribute it with credit.
