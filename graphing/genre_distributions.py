import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from random import choice

def main(filename):
        
    df = pd.read_csv(filename)
    # start year. we do 100 years until 2010. oldest film is from 2007.
    start = 1910
    genres = df["genre"].unique()
    genre = input(f"what genre? first letter capitalised. options: {genres}\n\n>>")

    # counts all movies per decade into a list.
    movies_per_decade = []
    i = 0
    while start + 10*i < 2010:
        movies_per_decade.append(df.loc[(start + 10*i <= df["year"]) & (df["year"] < start + 10*(i+1))].shape[0])
        i += 1

    # just an x-axis.
    x = [1910 + 10*j for j in range(10)]

    # here we pick number of movies in a given genre per decade into a list.
    specific_genre = []
    i = 0
    while start + 10*i < 2010:
        specific_genre.append(df.loc[(start + 10*i <= df["year"]) & (df["year"] < start + 10*(i+1)) & (df["genre"] == genre)].shape[0])
        i += 1

    # normalise by number of films per decade total so it's not biased like that.
    genre_percent = [a/b for a,b in zip(specific_genre, movies_per_decade)]

    # generates a normal distribution with peak 1. easier to scale the final product.
    # for smoothing.
    def gen_normal(mu, sigma, n):
        vec = np.linspace(1910,2010,n)
        return np.exp(-0.5 * np.square((vec-mu)/sigma))

    # new_dist is the smoothed distribution of genre_percent.
    new_dist = np.sum(size*gen_normal(1910 + 10*i, 5, 1000) for i, size in enumerate(genre_percent))
    X = np.linspace(1910,2010,1000)

    plt.plot(X, new_dist, color="black")
    plt.title(f"{genre} % per decade")
    plt.show()

if __name__ == "__main__":
    main("cleaned_titles_data.csv")
