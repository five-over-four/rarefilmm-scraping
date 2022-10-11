from random import choice
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tmdbsimple as tmdb
import requests

def get_genres(df):
    return df["genre"].unique()

def generate_distributions(df):
    
    # start year. we do 100 years until 2010. oldest film is from 2007.
    start = 1910
    genres = df["genre"].unique()

    # counts all movies per decade into a list.
    movies_per_decade = []
    i = 0
    while start + 10*i < 2010:
        movies_per_decade.append(df.loc[(start + 10*i <= df["year"]) & (df["year"] < start + 10*(i+1))].shape[0])
        i += 1

    # just an x-axis.
    x = [1910 + 10*j for j in range(10)]

    # here we pick number of movies in a given genre per decade into a list.
    genres_dist = {genre: [] for genre in genres}
    i = 0
    while start + 10*i < 2010:
        for genre in genres_dist:
            genres_dist[genre].append(df.loc[(start + 10*i <= df["year"]) & (df["year"] < start + 10*(i+1)) & (df["genre"] == genre)].shape[0])
        i += 1

    # normalise by number of films per decade total so it's not biased like that.
    genre_percents = {genre: [a/b for a,b in zip(genres_dist[genre], movies_per_decade)] for genre in genres}

    # generates a normal distribution with peak 1. easier to scale the final product.
    # for smoothing.
    def gen_normal(mu, sigma, n):
        vec = np.linspace(1910,2010,n)
        return np.exp(-0.5 * np.square((vec-mu)/sigma))

    smooths = dict()
    for genre, dist in zip(genre_percents.keys(), genre_percents.values()):
        smooths[genre] = np.sum(size*gen_normal(1910 + 10*i, 5, 1000) for i, size in enumerate(dist))

    return smooths

# this sets the scale on all the distributions to be so it integrates to 1.
def normalise(data):
    return data / (np.sum(data) / 1000)

def plott(data):
    X = np.linspace(1910,2010,1000)
    _, axes = plt.subplots(4, 10, figsize=(15,7))
    for genre, ax in zip(data, axes.flat):
        ax.plot(X, normalise(data[genre]), color="black")
        ax.xaxis.set_tick_params(labelbottom=False)
        ax.yaxis.set_tick_params(labelleft=False)
        ax.set_title(f"{genre}")
    plt.savefig("aaa.png")

def get_tmdb_films(genres):
    genres = genres
    for page in pages:
        s = "https://api.themoviedb.org/3/movie/top_rated?api_key=08bfcffdd73f2bfad0410dc1914be2c6&query=26&with_genres=28&page=1&include_adult=false"

if __name__ == "__main__":

    # this section makes sure we're only searching for genre names that exist on tmdb.
    # some of the uncommon ones that show up on rarefilmms, like "blaxploitation" do not
    # exist on tmdb, so we have to prune them. notice that Sci-Fi = Science Fiction.
    tmdb_genres = [{"id":28,"name":"Action"},{"id":12,"name":"Adventure"},
                            {"id":16,"name":"Animation"},
                            {"id":35,"name":"Comedy"},
                            {"id":80,"name":"Crime"},
                            {"id":99,"name":"Documentary"},
                            {"id":18,"name":"Drama"},
                            {"id":10751,"name":"Family"},
                            {"id":14,"name":"Fantasy"},
                            {"id":36,"name":"History"},
                            {"id":27,"name":"Horror"},
                            {"id":10402,"name":"Music"},
                            {"id":9648,"name":"Mystery"},
                            {"id":10749,"name":"Romance"},
                            {"id":878,"name":"Science Fiction"},
                            {"id":10770,"name":"TV Movie"},
                            {"id":53,"name":"Thriller"},
                            {"id":10752,"name":"War"},
                            {"id":37,"name":"Western"}]

    df = pd.read_csv("cleaned_titles_data.csv")
    genres = get_genres(df)
    genres = [genre for genre in genres if genre in [x["name"] for x in tmdb_genres]]
    genres.append("Sci-Fi")
    print(genres)

    #tmdb_data = get_tmdb_films(genres)
    rarefilmm_data = generate_distributions(df)
    plott(rarefilmm_data)