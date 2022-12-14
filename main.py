from flask import Flask, redirect, url_for, render_template, request
from test_scripts import collect_metadata as cm
from templates import generate_html as genhtml
import pandas as pd
from random import randint
import webbrowser
from test_scripts import movie_recommendation
from test_scripts import w2vsemanalysis as w2v
      
cm.API_KEY = "08bfcffdd73f2bfad0410dc1914be2c6"
cm.df = pd.read_csv("./data/rf_data.csv")

app = Flask(__name__)

def select_poster(df):
    """
    This just chooses either the RF or TMDB poster,
    priority for TMDB, if it exists.
    2496 / 2771 have a tmdb poster.
    """
    
    if len(str(df["poster"])) == 3:
        raw_df_movie = cm.df.loc[cm.df["title"]==df["title"]]
        return raw_df_movie["poster-path"]
    return df["poster"]

def select_genres(df):
    """
    Some movies don't have genres available on TMDB and only have the 
    RF genre. In this case, select the RF genre. Otherwise, get all the genres
    on TMDB.
    """
    # if (df.iloc[11:] == 0).all(): # this is the one-hot columns.
    #     return df["genre"]
    new_df = df.loc['Action':'Western']
    return ", ".join(new_df[new_df == 1].index.format())

def format_countries(df):
    new_df = df.loc['afghanistan':'zimbabwe']
    countries = new_df[new_df == 1].index.format()
    for i in range(len(countries)):
        countries[i] = countries[i].title()
    return ", ".join(countries)

def generate_background(df):
    """
    The random background picker, whenever the user refreshes.
    Just for fun.
    """
    n = df.shape[0] - 1
    return select_poster(df.iloc[randint(0,n)])

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
    return genhtml.generate_html_block({"poster": "http://rarefilmm.com/wp-content/uploads/2017/07/rrflogo.png",
            "score": "",
            "year": "",
            "title": "Welcome!",
            "overview": "Search for a movie below to get recommendations from the <a href='https://rarefilmm.com'>Rarefilmm</a> database! \
                        The recommendations will be based on various properties of the user's movie, such as description, genre(s), ratings...",
            "genre": "", 
            "country": ""})

def give_error_page():
    """
    Give this whenever no results are found. May not be useful in the final product,
    but proved interesting for testing purposes.

    We'll probably need *some* error page at the end, no matter what.
    """
    return genhtml.generate_html_block({"poster": "http://rarefilmm.com/wp-content/uploads/2017/07/rrflogo.png",
            "score": "",
            "year": "",
            "title": "Nothing found in the search!",
            "overview": "Your search yielded no results from the TMDB database; try a different query.",
            "genre": "",
            "country": ""})

def movies_to_html_block(movies, search_movie=None):
    """
    takes a list of rf_data.csv rows and turns them into
    html blocks that can be inserted into home.html, using
    generate_html.generate_html_block().
    """
    html_block = genhtml.generate_html_block({
                    "score": '',
                    "year": f"({search_movie['year']})",
                    "title": search_movie["title"], 
                    "poster": select_poster(search_movie), 
                    "overview": search_movie["description"],
                    "genre": f'Genres: {select_genres(search_movie)}',
                    "country": f'Countries: {format_countries(search_movie)}'
                }) + "<div class='title-box'></div><br>"
    for film in movies:
        html_block = html_block + \
                genhtml.generate_html_block({
                    "score": "",
                    "year": f"({int(film['year'])})",
                    "title": film["title"], 
                    "poster": select_poster(film), 
                    "overview": film["description"],
                    "genre": f'Genres: {select_genres(film)}',
                    "country": f'Countries: {format_countries(film)}'
                })
    return html_block


@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    """
    on localhost:5000/home or just localhost:5000.
    """

    background_poster = generate_background(movie_recommendation.df)
    search_report = "" # This says 'Recommendations based on x:' at the top after searching.

    # after a single search, it's always POST, since we keep resubmitting the request on each
    # refresh. so only on the first open, you get the instruction page. this MIGHT have to be
    # rewritten into a redirect scheme later.
    if request.method == "GET":
        display_html = give_front_page()

    # gets just one search result now. selects error page if not found,
    # otherwise shows the search result. will later update to showing
    # RECOMMENDATIONS (multiple).
    elif request.method == "POST":
        try:
            how_many_recommendations = int(request.form.get("number").strip())
        except:
            how_many_recommendations = 5
        search_movie = request.form.get("movies")
        try:
            search_movie_res, recommended_movies = movie_recommendation.get_movie_recommendations(search_movie, how_many_recommendations)
        except:
            search_movie_res, recommended_movies = None, None
            display_html = give_error_page()
            search_report = ""
        # movies = [cm.df.iloc[randint(0,cm.df.shape[0]-1)] for x in range(how_many_recommendations)] # totally just at random for now.
        if not recommended_movies: # nothing turned up.
            display_html = give_error_page()
            search_report = ""
        else:
            search_movie = search_movie_res.iloc[0]
            display_html = movies_to_html_block(recommended_movies, search_movie)
            search_report = f"Recommendations based on {search_movie['title']}:"

    return render_template("home.html", display_html=display_html, random_background=background_poster, search_report=search_report, numbers=[*range(1,11)])

@app.route("/info")
def info():
    """
    on localhost:5000/info. contains information about the project.
    """
    return render_template("info.html", random_background=generate_background(movie_recommendation.df))

if __name__ == "__main__":
    """
    Initialise front page,
    queue web browser,
    run flask app.
    """
    # uncomment if you want the browser to open here automatically.
    # NOT COMPATIBLE WITH HEROKU.
    #webbrowser.open_new_tab("http://127.0.0.1:5000")
    # w2v.initialize_docs()
    app.run(debug=False, port=5000)
   
