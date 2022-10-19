from flask import Flask, redirect, url_for, render_template, request
from templates import collect_metadata as cm
import pandas as pd
from random import randint

cm.API_KEY = "08bfcffdd73f2bfad0410dc1914be2c6"
cm.df = pd.read_csv("./data/rf_data.csv")

app = Flask(__name__)

def select_poster(df):
    """
    This just chooses either the RF or TMDB poster,
    priority for TMDB, if it exists.
    """
    if len(str(df["tmdb-poster"])) == 3:
        return df["poster-path"]
    return df["tmdb-poster"]

def generate_background():
    """
    The random background picker, whenever the user refreshes.
    Just for fun.
    """
    n = cm.df.shape[0] - 1
    return select_poster(cm.df.iloc[randint(0,n)])

def format_date(date):
    """
    As collect_metadata.get_movies() can return the film's date in either datetime.datetime
    or a year number, we gotta check for this. We don't want to print out the whole datetime object.
    """
    if len(str(date)) > 4:
        return str(date)[:4]
    return date

def give_front_page():
    """
    This is the default information on the /home page when first starting the application.
    """
    return {"poster": "http://rarefilmm.com/wp-content/uploads/2017/07/rrflogo.png",
            "year": "",
            "title": "Welcome!",
            "overview": "Enter a list of movies below to get a recommendation from the <a href='https://rarefilmm.com'>Rarefilmm</a> database! \
                        Separate your entries by commas. <br><br>Example: 'Taxi Driver, Synecodche new york, \
                        i'm thinking of ending things, It's such a beautiful day', without the single quotes."}

def give_error_page():
    """
    Give this whenever no results are found. May not be useful in the final product,
    but proved interesting for testing purposes.

    We'll probably need *some* error page at the end, no matter what.
    """
    return {"poster": "http://rarefilmm.com/wp-content/uploads/2017/07/rrflogo.png",
            "year": "",
            "title": "No movies found!",
            "overview": "Your search yielded no results from the TMDB database; try a different query."}

@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    """
    on localhost:5000/home or just localhost:5000.
    """
    global movie_data

    background_poster = generate_background()

    # this currently just displays the first search result from tmdb with the given search terms.
    # useful for testing, but will change in the final product.
    if request.method == "POST":
        search = request.form.get("movies")
        search_terms = search.split(",")
        movies = cm.get_movies(search_terms, False)
        if all([movie.title == None for movie in movies]):
            movie_data = give_error_page()

        # TODO some kinda thing.
        else:
            movie = movies[0]
            movie_data = {"year": f"({format_date(movie.release_date)})", "title": movie.title, "poster": movie.poster, "overview": movie.overview}

    return render_template("home.html", movie=movie_data, random_background=background_poster)

@app.route("/info")
def info():
    """
    on localhost:5000/info. contains information about the project.
    """
    return render_template("info.html", random_background=generate_background())

if __name__ == "__main__":

    movie_data = give_front_page()
    # app.run() use this in the final product.
    app.run(debug=True)